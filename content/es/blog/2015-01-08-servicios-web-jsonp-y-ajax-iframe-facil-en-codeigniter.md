---
title: "Servicios web JSONP y AJAX – iframe fácil en CodeIgniter"
date: 2015-01-08T10:00:00+02:00
slug: "servicios-web-jsonp-y-ajax-iframe-facil-en-codeigniter"
aliases: ["/post/servicios-web-jsonp-y-ajax-iframe-facil-en-codeigniter"]
tags: [php, codeigniter, javascript, ajax]
description: "Técnicas de JSONP y subida de ficheros mediante iframe, y la librería Spark/ajax para generar respuestas en CodeIgniter."
legacy: true
cover: "https://www.sevir.org/content/images/20170813225053-ci_ajax_jsonp.jpg"
---
Aunque hace bastante tiempo de esto, aún tiene mucha utilidad. Se ha convertido en una costumbre que las aplicaciones webs estén pobladas de consultas o peticiones AJAX, cargando inicialmente una plantilla, y actualizando los contenidos mediante consultas o peticiones asíncronas.

Cuando queremos subir ficheros en segundo plano sin realizar la carga, en cambio no podemos usar AJAX, teniendo que remitirnos al File API de HTML5 o bien buscar una técnica alternativa que permita enviar un formulario con un formulario en multipart en segundo plano. Esto se puede conseguir mediante iframes, la técnica se basa en crear un iframe no visible (que no oculto, si está display:hidden no funcionará), de un tamaño de 0 pixeles y sin bordes conseguiremos un iframe funcional pero que no es visible por el usuario. Si indicamos como target de un formulario multipart este iframe, podremos subir un fichero sin recargar la página.

El problema será entonces conocer el momento en que el archivo se ha terminado de subir, para esto la respuesta cargada en el iframe debe ejecutar una llamada JavaScript definida en la ventana padre, que como si fuese una función de Callback se ejecutará cuando tengamos subido el fichero.

Poder obtener datos en JavaScript entre diferentes dominios permitirá crear fácilmente servicios web en formato JSON, a esta técnica se le denomina JSONP, consiste en devolver no un objeto JavaScript sino la llamada a una función con el nombre que escojamos (función callback) pasando como parámetro este objeto.
Cuando cargamos una url con la llamada al servicio lanzaremos la ejecución de la función de callback con los datos que esperamos de respuesta. Esto ya lo hace jQuery por detrás cuando ejecutamos el método $.getScript generando una función con un nombre aleatorio.

Para todo esto tenemos una librería que nos ayudará para generar respuestas en formato JSON, JSONP, XML y respuestas a través de iframes, si usamos CodeIgniter 2 o superior, mediante Spark/ajax disponemos de una serie de funciones helpers y métodos útiles para generar respuestas válidas en JSONP, envío de respuestas dentro de un iframe o respuestas en XML.

Con un método $this->ajax->response() podremos generar respuestas para enviar como JSON, JSONP, extender un objeto JS con jQuery, asignar datos generados a una variable, o generar respuestas en XML a partir de un objeto PHP.

Por ejemplo queremos cargar las cadenas de traducción de un array PHP a una variable JavaScript, podríamos añadir una carga de script en HTML

```html
<script type="text/javascript" src="http://url/controller/method">
```

y que este método PHP devuelva los datos en una variable:

```php
$this->ajax->response($array_traduccion, null, TRUE, "varjs");
```

Esto cargará los datos en varjs para poder usarlo en JavaScript. Esto funcionaría también en cualquier dominio, por lo que sería cross-domain.
