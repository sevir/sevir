---
title: "Magento convenciones y programación orientada a eventos"
date: 2015-10-15T10:00:00+02:00
slug: "magento-convenciones-y-programacion-orientada-a-eventos"
aliases: ["/post/magento-convenciones-y-programacion-orientada-a-eventos"]
tags: [php, magento, programacion]
description: "Reflexión sobre el uso de eventos en Magento y PHP frente a sobrescribir el core en las extensiones."
legacy: true
cover: "https://www.sevir.org/content/images/20170813231027-Magento-Logo2.jpg"
---
Son muchos los entornos que se han pasado a la programación orientada a eventos. Aunque de forma descafeinada, pues no siempre es lo que entendemos como eventos que se disparan y se ejecutan en segundo plano.

Llevo ya unas semanas intensivas desarrollando sobre Magento para cerrar un proyecto. Al igual que Wordpress, Magento tiene una serie de eventos sobre los que uno puede establecer sus rutinas que se ejecutarán cuando se lancen estos eventos.

Al contrario que en JavaScript, Node, C# y otros, los eventos en PHP se ejecutan de forma secuencial y nos sirven básicamente para ejecutar rutinas de código en mitad del código principal de la aplicación sin necesidad de tocar el core de la misma. Una clase que ejerce de controlador de eventos almacena todas las funciones de callback junto al evento con el que se tienen que ejecutar, y las lanza de forma secuencial cuando este evento es llamado.

A menudo es fácil darse cuenta que este tipo de programación no es la que estamos acostumbrados en PHP y he visto cantidad de código de extensiones que deciden sobreescribir todo el código antes que usar eventos, rompiendo así en ocasiones la funcionalidad de otras extensiones.

Siempre que trabajo con Software Libre y extensiones de terceros compradas, me viene la sensación que, aunque la funcionalidad esté desarrollada, el código a veces, dista de ser bueno, suponiendo auténticos quebraderos de cabeza al resto de desarrolladores.
