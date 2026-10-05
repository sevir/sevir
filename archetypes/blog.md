---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
tags: []
description: ""
# cover: "images/blog/mi-imagen.jpg"
draft: true
---

{{ "{{< caption >}}" }}Mientras tanto, en el laboratorio…{{ "{{< /caption >}}" }}

{{ "{{< bubble >}}" }}¡Hola! Hoy toca…{{ "{{< /bubble >}}" }}

Texto del episodio. Usa {{ "{{< sfx \"¡BOOM!\" >}}" }} para las onomatopeyas.
