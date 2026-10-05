---
title: "El auge de los generadores de sitios en texto plano"
date: 2017-08-25T10:00:00+02:00
slug: "el-auge-de-los-generadores-de-sitios-en-texto-plano"
aliases: ["/post/el-auge-de-los-generadores-de-sitios-en-texto-plano"]
tags: [web, blog, markdown, hugo]
description: "Repaso a los Flat File CMS y generadores de webs estáticas basados en Markdown, con Hugo como gran recomendado."
legacy: true
cover: "https://www.sevir.org/content/images/20170814173118-maxresdefault.jpg"
---
Hace ya casi una década cuando uno desarrollaba su página web con Dreamweaver o con FrontPage.

Como todo lo antiguo vuelve, en pleno *siglo 21th* y tras haber superado la web 2.0 y la 3.0 resulta que lo *cool* ahora es editar de nuevo tu web en local o a través de tocar los ficheros de contenido directamente.

Y aunque hay algunas diferencias, y ha llovido mucho, volvemos a escribir contenido web desde nuestro ordenador y una aplicación de escritorio.

Los motivos son muy diferentes. Y aunque el porcentaje de penetración de Wordpress y otros blogs de edición online siguen siendo mayoritarios, ahora tenemos entornos completos de creación de webs sin necesidad de bases de datos, loque ahora se llama **Flat-File-CMS** o **Static Web Generators**.

Tenemos que distinguir entre dos tipos. Sistemas desarrollados en PHP que trabajan con ficheros de texto, y generadores de webs.
y
En ambos casos de forma predominante, el contenido se escribe en formato **Markdown**, pero el resultado es diferente a la hora de trabajar, aunque visualmente un usuario no podría distinguir si una web está hecha con un sistema u otro.

La ventaja, además de poder escribir más rápido y concentrarse en el contenido y no en la forma en que se muestra, es que, al no usar base de datos, la carga de la web es mucho más rápida.

Por otro lado las webs generadas estáticamente ni tan siquiera necesitarían de PHP, u otro soporte de lenguaje de programación en el servidor web. Cualquier espacio web incluso Github podría ser hosting para este tipo de webs.

Del primer grupo estos serían los proyectos más interesantes:

## Flat File CMS

- [Pico CMS](http://picocms.org). Es todo un clásico, funciona sobre PHP con plantillas TWIG, soporte de contenido en Markdown y un buen puñado de templates.
- [HTMLy](https://www.htmly.com). Más reciente, permite editar online el contenido y tiene interfaz de administración. Este blog está funcionando sobre este proyecto.
- [Grav](https://getgrav.org). Un proyecto interesante, también funcionando sobre Twig, Symfony y muy extensible con una buena cantidad de plugins. También permite edición online así como configuración con ficheros YAML, generación de tipos especiales de contenido. En definitiva,un sistema muy versátil.
- [Dokuwiki](https://www.dokuwiki.org/dokuwiki). Lleva años con nosotros, un wiki rápido de editar, ideal para documentar proyectos, edición online y todo almacenado sobre ficheros. El backup es trivial, solo hay que copiar toda la carpeta a otro sitio para tenerlo funcionando.

## Static Web Generators

- [Hexo](https://hexo.io). Genera una web estática con NodeJS. Dispone de diferentes temas para modificar el aspecto del resultado.
- [WinterSmith](http://wintersmith.io). También sobre NodeJS, fue de los pioneros aunque muy básico comparado con los demás.
- [MkDocs](http://www.mkdocs.org). Si has escrito documentación en Markdown,seguro que te suena, o al menos su theme por defecto, multitud de proyectos lo usan para generar la web de documentación. Funciona sobre Python, que necesitarás tener instalado.
- [Sculpin](https://sculpin.io). Sobre PHP y TWIG, genera webs estáticas, y no necesitarás posteriormente PHP para visualizar el resultado.
- [Hugo](http://gohugo.io). El ganador por goleada es Hugo,un sistema versátil, al estar hecho en GO, solo necesitas un ejecutable disponible en Windows, Linux y Mac para generar tu web a partir de Markdown. Tiene un catálogo de *themes* impresionante para el poco tiempo que lleva. Sin duda el más recomendable.

Ahora solo te queda elegir el que más te guste.
