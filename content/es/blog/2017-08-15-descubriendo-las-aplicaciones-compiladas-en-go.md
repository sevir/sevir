---
title: "Descubriendo las aplicaciones compiladas en Go"
date: 2017-08-15T10:00:00+02:00
slug: "descubriendo-las-aplicaciones-compiladas-en-go"
aliases: ["/post/descubriendo-las-aplicaciones-compiladas-en-go"]
tags: [go, herramientas, devops]
description: "Selección de aplicaciones escritas en Go, compiladas en un único ejecutable, que uso en desarrollo y sistemas."
legacy: true
cover: "https://www.sevir.org/content/images/20170814172620-bumper.jpg"
---
Hace poco tiempo que estoy profundamente interesado en Go, no tanto como lenguaje, que me parece atractivo, sino todas las aplicaciones que se han creado con este lenguaje.

La principal ventaja de las aplicaciones creadas con Go es que se compilan en un solo ejecutable, por lo general puedes compilar ejecutables para Windows, Linux y MacOSX con el mismo código, simplemente diciendo al compilador, para que sistema quieres sacarlo.

Luego Go es un lenguaje que genera código compilado próximo a C o C++, por lo que su velocidad de ejecución es muy rápida, y además pensado para facilitar las tareas concurrentes utilizando varios procesadores. El resultado es siempre unas aplicaciones de gran rendimiento y escalabilidad.

El sitio para buscar aplicaciones hechas en Go es [GoLandLibs](https://golanglibs.com), busca por la etiqueta *applications*.

Estas son las aplicaciones en Go que más me gustan y uso:

- [Sup](https://pressly.github.io/sup/). Una herramienta tipo Deployer para lanzar comandos remotos a multitud de servidores en paralelo, como hace Ansible, Capistrano, Deployer, y otros, pero más sencillo y rápido.
- [Capze](https://github.com/yuuki/capze). Genera una estructura de despliegue tipo Capistrano rápidamente, se integra muy bien con **Sup**.
- [Restic](https://restic.github.io). Permite generar backups y backups incrementales rápidamente, más rápido que duplicity.
- [Duplicacy](https://github.com/gilbertchen/duplicacy). Aún mejor que Restic, permite subir el backup a múltples servicios online de disco: S3, Onedrive, Google Drive, Dropbox, FTP, etc...
- [LNAV](http://lnav.org). Un visor de logs hypervinaminado, multitud de utilidades como leer directamente de históricos guardados en TGZ sin tener que cambiar de fichero.
- [Hugo](https://gohugo.io). Un generador de webs estáticas. Para qué necesitas Wordpress si puedes tener algo como esto...
- [Fast Reverse Proxy](https://github.com/fatedier/frp). Permite montar un proxy que exponga los puertos de ordenadores dentro de un NAT a una IP pública. Muy rápido y gran utilidad para desarrollar servicios web en modo pruebas.
- [Minio](https://www.minio.io). Directamente todo un servidor S3 personal en un solo ejecutable. Impresionante.
- [Caddy](https://caddyserver.com/features). Un servidor web con soporte para HTTP2, certificados, gran rendimiento y fácil configuración en un solo fichero. Lo uso principalmente para no tener que montar un Apache o Nginx en un entorno de desarrollo, el fichero de configuración puede ir en el mismo repo GIT y arrancar el proyecto en segundos arrancando las dependencias al mismo tiempo (servidor MySQL, Redis, o lo que sea).
- [NATS](http://nats.io). Uno de los grandes descubrimientos, gestiona un sistema de paso de mensajes Pub-Sub y gestión de colas de forma instantánea sin grandes requerimientos como pasa con RabbitMQ. Permite montar cluster del servicio de forma sencilla y aguanta cientos de miles de mensajes por segundo.
- [Aurora](https://xuri.me/aurora/). Si buscas un servidor de Beanstalk rápido y sencillo esto es lo que necesitas.
- [Fabio](https://github.com/fabiolb/fabio). Un balanceador para microservicios web. Muy rápido.
- [MeshBird](http://meshbird.com). Genera una red virtual distribuida entre tus servidores, contenedores Docker, ordenadores personales y lo que quieras. Muy bueno.
- [GoRush](https://github.com/appleboy/gorush). Un servidor de notificaciones push propio, para no depender de Pushbush y otros...
- [ImageServer](https://github.com/pierrre/imageserver). Todo lo que necesitas para recortar, retocar imágenes, resamplear y lo que te imagines como microservicio web con API.
- [Flynn](https://flynn.io). Escala de forma horizontal servidores de bases de datos o aplicaciones a través de contenedores docker de forma transparente y automática.
- [GoGS](https://gogs.io). Impresionante, tu propio Github, mil veces más fácil de instalar que Gitlab.

Como veréis hay proyectos muy interesantes usandose en sistemas de producción enormes. y con una fiabilidad asombrosa.

Habrá que estar atentos a los proyectos que vayan surgiendo con este lenguaje.
