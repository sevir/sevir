---
title: "Incrementando la velocidad del log de PHP en nuestro proyecto web"
date: 2015-02-01T10:00:00+02:00
slug: "incrementando-la-velocidad-del-log-de-php-en-nuestro-proyecto-web"
aliases: ["/post/incrementando-la-velocidad-del-log-de-php-en-nuestro-proyecto-web"]
tags: [php, codeigniter, redis, rendimiento]
description: "Benchmark del log en CodeIgniter comparando ficheros, SQLite y Redis, con Redis como opción más rápida."
legacy: true
cover: "https://www.sevir.org/content/images/20170813225806-php_log_redis.jpg"
---
Recientemente trabajamos sobre un framework desarrollado por el equipo de [Emagister](http://engineering.emagister.com/) y como es normal aunque tiene similitudes en cuanto a características con nuestro framework Creamture, hay otras cosas que son diferentes y no encontramos un rendimiento óptimo.

Una de estas cosas es el tema del log de errores utilizando para ello una tabla en base de datos. El uso de base de datos para escribir en un log es bastante lento comparado con la escritura directamente en un fichero en disco, aunque mantiene algunas esperadas ventajas como la posibilidad de disponer de un visor de log mediante consultas SQL, lo que permite lectura únicamente de las entradas ordenadas por fecha, paginación, sin tener que volcar todo el fichero de log que podría ser muy grande. Aunque la escritura en base de datos es mucho más lenta que la escritura en fichero, el impacto no es muy grande pues únicamente pasan a log los errores o excepciones.

CodeIgniter, y Creamture crea un fichero de log en formato texto por cada día, lo que minimiza que los ficheros crezcan excesivamente, pero al usar el log no solo para volcar errores graves sino como bitácora para cualquier tipo de información que los desarrolladores queremos visualizar, podemos encontrarnos con ficheros diarios de varios megas.

Reciéntemente he mejorado el visor de log que teníamos en Creamture, que permite visualizar los ficheros de los logs de CI 1.7 hasta CI 2.2 (Creamture). Disponiendo de un modo para visualizar el log actual en tiempo real, realizando lecturas parciales del fichero en disco. Podéis descargarlo [este GIST](https://gist.github.com/sevir/bbfa3b66dae047978696).

El caso es que pensando en cómo mejorar, esta tarde me dispuse hacer un pequeño test utilizando una instalación base de CodeIgniter 1.7. Se me ocurrió que podría ser más práctico si se usaba un sistema de almacenamiento más organizado y mejor que un fichero, pero que siga siendo más rápido que una base de datos.

## El impacto del log normal sobre un controlador

Activando únicamente el log de errores, y no de debug ni info, para minimizar el impacto (CodeIgniter genera log de debug al pasar por casi cualquier librería), y creamos un controlador con un método muy muy simple:

```php
function index()
{
    echo 'OK';
}
```

Usaremos para probar el funcionamiento normal en nuestro sistema, un pequeño programa para nodejs, llamado [webstress-tool](https://www.npmjs.com/package/webstress-tool) con el que podemos lanzar peticiones concurrentes y obtener una media de las mismas, generaremos 10 bloques de peticiones de 50 peticiones concurrentes, cada bloque estará separado por 1 segundo de diferencia.

```
$ webstress GET http://www.ci17.com 10 50
about to send 500 GET requests to url http://www.ci17.com over 10 seconds
done, took total over: 12034, avg response time: 240.68
done, took total over: 8849, avg response time: 176.98
done, took total over: 7800, avg response time: 156
done, took total over: 7804, avg response time: 156.08
done, took total over: 7686, avg response time: 153.72
done, took total over: 7636, avg response time: 152.72
done, took total over: 7701, avg response time: 154.02
done, took total over: 7713, avg response time: 154.26
done, took total over: 7171, avg response time: 143.42
done, took total over: 7073, avg response time: 141.46
```

Entonces modifiqué nuestro pequeño método para añadir una llamada a log_message: `log_message('ERROR', 'Hola mundo!');` con lo que al probar de nuevo, encontramos cómo afecta el log a la media de las respuestas:

```
$ webstress GET http://www.ci17.com 10 50
about to send 500 GET requests to url http://www.ci17.com over 10 seconds
done, took total over: 15360, avg response time: 307.2
done, took total over: 10872, avg response time: 217.44
done, took total over: 11044, avg response time: 220.88
done, took total over: 11931, avg response time: 238.62
done, took total over: 11037, avg response time: 220.74
done, took total over: 10955, avg response time: 219.1
done, took total over: 11189, avg response time: 223.78
done, took total over: 12869, avg response time: 257.38
done, took total over: 11121, avg response time: 222.42
done, took total over: 11744, avg response time: 234.88
```

Podemos ver como una única llamada al log tiene un importante impacto aunque la llamada sea simple. Por lo que no podemos ignorar que aún utilizando ficheros de texto, el impacto es significativo.

## Probando con SQLite

La idea es generar un fichero de SQLite por día, y poder guardar la misma información que los ficheros de log, para eso creamos un método log_message alternativo que abrirá una bbdd sqlite nombrada con la fecha actual, intentamos siempre insertar, en caso de error crearemos la tabla ya que el error será por no existir la tabla, pero será más rápido que comprobar siempre si la tabla existe.

El resultado es desalentador:

```
$ webstress GET http://www.ci17.com 10 50
about to send 500 GET requests to url http://www.ci17.com over 10 seconds
done, took total over: 30964, avg response time: 619.28
done, took total over: 27871, avg response time: 557.42
done, took total over: 30341, avg response time: 606.82
done, took total over: 28935, avg response time: 578.7
done, took total over: 24958, avg response time: 499.16
done, took total over: 27928, avg response time: 558.56
done, took total over: 21769, avg response time: 435.38
done, took total over: 23220, avg response time: 464.4
done, took total over: 26227, avg response time: 524.54
done, took total over: 25003, avg response time: 500.06
```

Sí sería posible leer el log mediante un visor con consultas SQL, pero la penalización por insertar una simple entrada resulta excesiva.

## Usando Redis para guardar el log

Después de leer la velocidad con la que funcionan los sistemas noSQL de almacenamiento key,value probamos Redis, cuyo funcionamiento es muy muy simple, y tenemos una librería muy probada para PHP.

Así que después de bajarnos una versión de Redis para Windows (existe versión para cualquier Unix, OSX y una compilación para Windows que ocupa algo menos de 2 megas.

El nuevo método que construimos es muy simple:

```php
function log_message2($level = 'error', $message, $php_error = FALSE)
{
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    $redis->lpush('ci17-'.(date('Y-M-d')), (date('Y-M-d H:i:s')).' - '.$level.' --> '.$message);
}
```

El resultado es casi tan bueno que el impacto sobre la versión sin log es mínimo, y además podemos recuperar las entradas rápidamente ordenadas por fecha y pudiendo paginar. Vemos que efectívamente Redis es muy útil si queremos guardar una bitácora para proyectos web de uso intensivo.

```
$ webstress GET http://www.ci17.com 10 50
about to send 500 GET requests to url http://www.ci17.com over 10 seconds
done, took total over: 10579, avg response time: 211.58
done, took total over: 8524, avg response time: 170.48
done, took total over: 8419, avg response time: 168.38
done, took total over: 8616, avg response time: 172.32
done, took total over: 8254, avg response time: 165.08
done, took total over: 8351, avg response time: 167.02
done, took total over: 8383, avg response time: 167.66
done, took total over: 8320, avg response time: 166.4
done, took total over: 8017, avg response time: 160.34
done, took total over: 7932, avg response time: 158.64
```

Lo próximo será actualizar nuestro framework y el visor de logs para usar Redis y establecer un fallback para utilizar ficheros en caso de no detectar un servidor Redis funcionando.
