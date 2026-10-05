# AGENTS.md · sevir.org (Dr. SeViR)

Guía para agentes que modifiquen la web personal de José Francisco Rives (SeViR): portada animada en SVG
con estética de manga retro, el laboratorio de inventos, la historia, el nivel de poder y el cuaderno
(blog) con los posts rescatados de *SeViR Notes*.

Este repositorio es el **repositorio de usuario de GitHub** (`sevir/sevir`): sirve a la vez de ficha de
perfil y de fuente de la web.

- `README.md` es la **ficha del perfil de GitHub**. No lo uses como documentación de la web ni lo
  sobrescribas al cambiar la web.
- La documentación de la web está en este fichero (`AGENTS.md`).

## Stack

- **Hugo extended 0.160.1** con el tema propio `themes/manga-lab`. No usa módulos de Hugo ni Node.
- Publicación en **GitHub Pages** con GitHub Actions (`.github/workflows/pages.yaml`), en cada push a `main`.
  Las actions deben estar en versiones que usen el runtime Node 24 (checkout v7, configure-pages v6,
  upload-pages-artifact v5, deploy-pages v5, peaceiris/actions-hugo v3).
- Dominio propio: `static/CNAME` = `www.sevir.org`; `baseURL` en `hugo.toml`. En el build, la URL base
  la pone `configure-pages`.

## Tareas

```sh
hugo serve           # http://localhost:1313 (es) y http://localhost:1313/en/ (en)
hugo --gc --minify   # build en ./public (ignorado por git)
hugo new content blog/$(date +%F)-mi-nuevo-post.md   # nuevo post (draft: true, con ejemplos de shortcodes)
./scripts/rescue-legacy-images.sh                    # descarga imágenes del blog antiguo a static/images/legacy/
```

Antes de dar por buena una modificación, ejecuta `hugo --gc --minify` y comprueba que termina sin errores
ni avisos nuevos.

## Idiomas

Español (por defecto, sin prefijo) e inglés (`/en/`). El blog solo existe en español; la sección inglesa
muestra los posts españoles con un aviso.

- Toda cadena de interfaz va en `i18n/es.yaml` y `i18n/en.yaml` (añádela siempre en los dos).
- Los datos en `data/*.yaml` llevan campos `{es, en}`.

## Diseño "Manga Lab" (v3: mundo SVG + familia vectorizada)

Personajes, pueblo y nombres son propios: no usar personajes, logotipos ni nombres de obras existentes.

- **Portada**: `themes/manga-lab/layouts/_partials/world.html` dibuja el mundo en capas `<svg>`
  independientes (cielo, montañas, colinas y pueblo, laboratorio, suelo) y `family.html` coloca encima a la
  familia y el primer plano. Cada capa tiene `--d` (profundidad) para el parallax con el puntero y el scroll
  (`assets/js/main.js`). Viewbox del mundo: 1600×900; las capas sobresalen un 4% por lado.
- **Personajes**: `static/images/chars/*.svg`, vectorizados desde la ilustración (ver `scripts/characters/`).
  Se animan como `<img>` (composición por GPU): cuerpo y cabeza son la misma imagen recortada por el cuello
  (`--neck`), la cabeza gira sobre su pivote, parpadeos con párpados SVG (`.lid`) y lengua del perro aparte.
  Datos (cajas, cuello, ojos, cabeza) en `data/chars.yaml`. Escala/posición de la familia en `family.html`.
  Los scripts de `scripts/characters/` tienen rutas absolutas de otra máquina (`/home/claude/sevir.org/`):
  ajústalas antes de regenerar.
- **Encuadres** de personajes en viñetas: `partial "crop.html" (dict "chars" (slice …) "rect" (slice x y w h))`
  en píxeles de la ilustración. `head-face.html` = cara del doctor (logo, línea temporal, 404, bocadillos).
- Tokens en `assets/css/00-tokens.css`; el CSS se concatena por nombre de fichero; `js/*.js` en `js/manga-lab.js`.
- Componentes: `.panel`, `.mp`/`.mpage` (página de manga), `.caption`, `.bubble`/`.mbubble`, `.msfx`,
  `.speedlines`, `.stamp`, `.pop`.
- Las animaciones respetan `prefers-reduced-motion` y el botón de pausa (`html[data-motion=off]`).
- Fuentes auto-alojadas (SIL OFL): Bangers, M PLUS Rounded 1c, Comic Neue, Dela Gothic One (subconjunto
  latino + kana). No enlaces fuentes ni scripts externos.

## Reglas de plantillas

- URLs siempre con `relURL` / `.RelPermalink`.
- Convierte a `float` los números de YAML antes de restar.

## Contenido

- Posts en `content/es/blog/AAAA-MM-DD-slug.md`. `cover` en el front matter = imagen de cabecera.
- Los posts rescatados llevan `legacy: true` y `aliases` a `/post/<slug>` (URLs del HTMLy antiguo), así
  las URLs antiguas redirigen a `/blog/<slug>/`. Mantén esos alias.
- Las imágenes antiguas apuntan a `https://www.sevir.org/content/images/...`; `rescue-legacy-images.sh`
  las descarga y reescribe las rutas. Si falta alguna, la tarjeta muestra la portada de color.
- Shortcodes: `caption`, `bubble`, `sfx`.

## Dónde se edita cada cosa

| Qué | Dónde |
|---|---|
| Ficha de personaje, intro y frases de los personajes al hacer clic | `data/profile.yaml` |
| Inventos (portada y `/laboratorio/`) | `data/inventions.yaml` |
| Línea temporal (capítulo 3) — **pendiente de completar con LinkedIn** | `data/timeline.yaml` |
| Nivel de poder | `data/powers.yaml` |
| Textos de la interfaz | `i18n/es.yaml`, `i18n/en.yaml` |
| Sobre mí | `content/es/sobre-mi.md`, `content/en/about.md` |
| Posts | `content/es/blog/` |
| Mundo animado de la portada | `themes/manga-lab/layouts/_partials/world.html` y `family.html` |
| Personajes vectorizados | `static/images/chars/` + `data/chars.yaml` (se regeneran con `scripts/characters/`) |
| Estilos y animaciones | `themes/manga-lab/assets/css/*.css` |
| Interacción (bocadillos, tema, scroll) | `themes/manga-lab/assets/js/main.js` |
| Ficha del perfil de GitHub (no es la web) | `README.md` |

## Despliegue

1. *Settings → Pages → Source: GitHub Actions* en este repositorio.
2. *Settings → Pages → Custom domain*: `www.sevir.org`.
3. DNS: `www` → CNAME a `sevir.github.io`; el apex `sevir.org` con los registros A/AAAA de GitHub Pages
   para que redirija a `www`.
