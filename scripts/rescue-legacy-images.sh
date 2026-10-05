#!/usr/bin/env bash
# Descarga las imágenes del blog antiguo (www.sevir.org/content/images/...) a
# static/images/legacy/ y reescribe las rutas en los posts.
# Ejecutar UNA VEZ antes de apuntar el dominio a GitHub Pages (después ya no existirán).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p static/images/legacy
grep -rhoE 'https://www\.sevir\.org/content/images/[^") ]+' content/ | sort -u | while read -r url; do
  f="static/images/legacy/$(basename "$url")"
  [ -f "$f" ] || { echo "↓ $url"; curl -fsSL "$url" -o "$f" || curl -fsSL "${url/https:/http:}" -o "$f" || echo "  ✗ no se pudo descargar"; }
done
# Reescribe solo las URLs cuyo fichero se ha descargado.
for f in static/images/legacy/*; do
  [ -e "$f" ] || continue
  name=$(basename "$f")
  grep -rl "https://www.sevir.org/content/images/$name" content/ | xargs -r sed -i "s#https://www.sevir.org/content/images/$name#/images/legacy/$name#g"
done
echo "Listo. Revisa los cambios con: git diff --stat"
