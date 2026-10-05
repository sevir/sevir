---
title: "Deployer, una buena alternativa a Capistrano"
date: 2015-02-14T10:00:00+02:00
slug: "deployer-una-buena-alternativa-a-capistrano"
aliases: ["/post/deployer-una-buena-alternativa-a-capistrano"]
tags: [php, deploy, devops, herramientas]
description: "Deployer como alternativa en PHP a Capistrano para despliegues atómicos con releases y rollback inmediato."
legacy: true
cover: "https://www.sevir.org/content/images/20170813225940-deployer.jpg"
---
Durante mucho tiempo hemos dado vueltas en DIGIO a cómo hacer un mejor deploy de los proyectos en el servidor. Nuestra forma de trabajar era sobre un repositorio GIT que se actualizaba desde el servidor con un simple `git pull` de forma que en caso de problemas podríamos hacer un reset a una versión dentro del histórico de GIT.

Además añadimos algunas cosas más como cargar configuración de cron a través de un fichero .crontab dentro del proyecto de forma que se actualizan los procesos por cron cada vez que hacemos un deploy. También un fichero .deploy que actúa como script de shell permitía ejecutar acciones una vez se había actualizado el código, para hacer migraciones de base de datos por ejemplo o borrar los ficheros de cache.

El mayor problema que veía es en proyectos con mucha afluencia de usuarios, si estamos actualizando el código, puede llegar una petición donde parte del código está actualizado, pero otras partes no, JavaScript, controladores, modelos, etc... Esto puede producir fallos en el sistema por tener código a medio utilizar e incidencias en los usuarios.

En mi última visita a Emagister en Barcelona, me contaron que ellos usaban Capistrano y Jenkins, el proceso de deploy es similar en cuanto podemos lanzar migraciones, y ejecución de otras tareas, pero resolvía el problema que teníamos nosotros de dar la posibilidad de tener código a medio actualizar cuando llega una petición web.

### Capistrano, herramienta de deploy sobre múltiples servidores en Ruby

Capistrano genera una carpeta de release con código nuevo (por lo general de un repositorio GIT), y no se hace el cambio en la carpeta raíz hasta que no se haya copiado todo a la nueva carpeta de release, pudiendo configurar cuántas carpetas de releases queremos conservar así como la posibilidad de volver hacia atrás en caso de error de forma inmediata simplemente apuntando el DocumentRoot a la carpeta de release anterior.

Pero tengo una pequeña manía y es que, siendo desarrollador PHP y JS, intento buscar siempre una alternativa a tener que instalar un intérprete de Ruby, Python o cosas similares, igual que no me gustan los Frameworks que trabajan con XML, YAML y PHP al mismo tiempo cuando se puede hacer todo en un solo lenguaje.

Y buscando buscando encontré un par de proyectos interesantes: [Rocketeer](http://rocketeer.autopergamene.eu/#/docs/rocketeer/README) y [Deployer](http://deployer.org/), pero quizás este último por su simplicidad, y por, admitámoslo, tiene una página web más agradable de leer, fue el que más me gustó.

Ambos proyectos son una copia de Capistrano, ambos funcionan con un phar como Composer, por lo que es muy cómodo y solo necesitamos un fichero para poder ejecutarlo. Quizás Deployer tiene algo más de versatilidad con menos configuración.

### Deployer versátil y fácil de configurar en PHP

Con Deployer asegurarmos un proceso de deploy seguro, posibilidad de revertir al instante a una versión anterior, lanzar comandos fácilmente en el servidor remoto o en el servidor de deploy, soporte para claves SSH, usuario y password y múltiples servidores por entorno (por ejemplo poder lanzar nuevos cambios a varios servidores de nuestro cluster).

Con Deployer definimos entornos (producción, desarrollo), dentro de cada uno, definimos un grupo de servidores sobre los que mandaremos actualizaciones (normalmente solo hay uno), y finalmente tareas para lanzar a estos servidores. Que en nuestro caso es enviar la última versión del código en Git.

Si juntamos esto con Jenkins o nuestra herramienta de deploy online podremos actualizar el código de nuestro proyecto fácilmente por todo el equipo.
