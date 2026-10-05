---
title: "Introducción a Vagrant, la mejor forma de preparar un proyecto web. Parte I"
date: 2015-08-17T10:00:00+02:00
slug: "introduccion-a-vagrant-la-mejor-forma-de-preparar-un-proyecto-web-parte-i"
aliases: ["/post/introduccion-a-vagrant-la-mejor-forma-de-preparar-un-proyecto-web-parte-i"]
tags: [vagrant, virtualizacion, devops]
description: "Introducción a Vagrant para crear entornos de desarrollo web homogéneos y distribuibles con máquinas virtuales."
legacy: true
cover: "https://www.sevir.org/content/images/20170813230715-Solucionar-archivos-corruptos-en-VirtualBox-y-Vagrant.png"
---
Y es que después de su par de años de maduración, Vagrant ya es una de las herramientas más utilizadas por todos los desarrolladores web, administradores de sistemas y cualquier profesional IT que quiera testear un entorno de servidores, ya sea Linux o Windows (aunque principalmente Linux).

Para que el que no lo conozca, Vagrant es una herramienta que permite generar una máquina virtual (para Virtualbox, VirtualPC o VMWare) preconfigurada y con acceso remoto, en unos pocos minutos, y fácilmente distribuible.

¿Para qué sirve?. Bien, pensemos que estamos desarrollando una página web en PHP, y necesitaremos por tanto en nuestro ordenador poder disponer de un servidor web con PHP y seguramente MySQL. Esto en el mejor de los casos, porque realmente nos podríamos encontrar con entornos con Dyango, RubyOnRails, NodeJS y alguno de sus innumerables frameworks web. Instalar todo esto en nuestro ordenador de trabajo además de ser tedioso, termina siendo insufrible debido a las diferencias en entornos Windows, Linux y OSX, cuando al final tendrá que estar funcionando sobre un servidor Unix de un hosting.

Hasta hace muy poco, la mayoría acudíamos a algún entorno LAMP (si hablamos de Apache+PHP+MySQL), un WAMP (en Windows) o quizás un MAMP (en OSX). Esto era bastante fácil, pero si tu proyecto empezaba a requerir más requisitos en cuestión de nuevos módulos de PHP, acceso a indexadores como ElasticSearch, Sphinx, etc... la instalación y compilación de estos módlos y dependencias se iba complicando.

A esto sumamos a este bonito cuadro, que nuestros compañeros con los que trabajamos en el mismo proyecto, uno tiene un Mac, otro un Windows y otro quizás un Linux. Resultaba imposible ayudar a nuestro compañero dándole instrucciones de cómo han montado el entorno, puesto que cada uno lo ha hecho en su propio sistema operativo.

Vagrant nos elimina todos estos problemas además de poder generar un entorno homogéneo para todo el equipo y que puede ser un clon de lo que tendremos en nuestro servidor más adelante a la hora de publicar nuestro proyecto en producción. Podremos pasar la configuración de nuestra máquina Vagrant, y un proceso de setup que instalará todo el entorno que necesitemos.

Lo primero que necesitamos saber es que podemos usar Vagrant de muchas maneras. La primera es instalar un sistema base, por ejemplo Ubuntu 14.04 escribiendo:

```bash
mkdir ubuntu
cd ubuntu
vagrant init precise32
```

Esto nos creará un fichero **Vagrantfile**, que podemos editar con un editor de texto.Desde este fichero podemos modificar la memoria RAM asignada, asignar carpetar compartidas, etc...

Una vez configurado podemos ejecutar:

```bash
vagrant up
```

Todos los comandos de vagrant deberemos ejecutarlos sobre la carpeta donde tenemos el Vagrantfile, de otra manera Vagrant no sabrá con que maquina virtual está trabajando. Esto descarga Ubuntu, y genera una máquina virtual ya preinstalada con este SO. Podremos entrar en la máquina virtual a través de SSH por línea de comandos, aunque si nunca hemos manejado un linux, es posible que se nos atragante.

```bash
vagrant ssh
```

Aquí tenemos una ligera diferencia, si usamos Windows, no tenemos de serie un cliente SSH, por lo que necesitaremos o bien instalar CygWin, GIT for Windows, o mejor aún [Babun](http://babun.github.io) (una versión retocada de CygWin mejorada para Windows de la que hablaré próximamente).

Una vez instalado en Windows, con Babun podremos trabajar normalmente.

Lo interesante aquí es que podamos generar una máquina virtual que nos permita que no trabajemos continuamente con la línea de comandos, y que podamos configurar el servidor fácilmente desde una interfaz web.

Podemos sobre este sistema base configurarlo y posteriormente exportarlo como un fichero .box que podemos pasar al resto del equipo, una vez tenemos exportada la máquina virtual, podemos compartirla con la comunidad desde la web de Hashcorp, la empresa que está detrás de Vagrant, de forma gratuita.

He compartido una máquina Vagrant que tiene lo necesario para trabajar con Apache, Nginx, PHP 5.5, MySQL (MariaDB 5.5), NodeJS, Composer, Bower.

Podéis descargarla en: <https://github.com/sevir/vagrant-webserver> una vez descargado, entrar en la carpeta para ejecutar un *vagrant up*.

Esta máquina virtual además de llevar preinstalado gran parte del sistema, actualiza e instala ciertos componentes en el momento de generar una nueva máquina virtual. A esto le llamamos **provisioning**, con Vagrant podemos provisionar un servidor de varias maneras, la más sencilla es ejecutar scripts de shell con los comandos que nosotros queramos, otra forma es utilizar algún software de provision de servidores como Puppet, Chef o Ansible de los que hablaremos próximamente.

_Actualización:_ Esta mañana en el trabajo me han hablado de la existencia de una extensión para Vagrant que podemos instalar para mantener siempre actualizada la versión de las VBGuest Additions que instalan mayor soporte para VirtualBox en la máquina virtual (en resumen hace que vaya más rápida). Simplemente ejecuta antes del vagrant up:

```bash
vagrant plugin install vagrant-vbguest
```
