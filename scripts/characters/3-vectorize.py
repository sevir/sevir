"""Vectoriza cada personaje de la ilustración (bordes de tinta + rellenos planos)."""
import numpy as np, cv2, vtracer, re, sys, json
from scipy.ndimage import binary_fill_holes
from PIL import Image

src0 = cv2.cvtColor(cv2.imread('/tmp/m/src.png'), cv2.COLOR_BGR2RGB)
fga = np.array(Image.open('/tmp/m/fg.png'))[:, :, 3]
lab = np.load('/tmp/m/labels.npy')
NAMES = ['dad', 'mom', 'kidA', 'kidB', 'dog']
S = 1.5
FILL = dict(filter_speckle=10, color_precision=6, layer_difference=26, corner_threshold=60,
            length_threshold=4.0, splice_threshold=45, path_precision=0, max_iterations=10)
LINE = dict(filter_speckle=5, corner_threshold=60, length_threshold=3.5, splice_threshold=45, path_precision=0)
KEY = np.array([255, 0, 255], np.uint8)


def body(svg):
    return re.sub(r'^.*?<svg[^>]*>|</svg>\s*$', '', svg, flags=re.S).strip()


def trace(img, **kw):
    h, w = img.shape[:2]
    px = [tuple(int(v) for v in p) + (255,) for p in img.reshape(-1, 3)]
    return vtracer.convert_pixels_to_svg(px, (w, h), **kw)


def scale_paths(svg_body, s):
    # vtracer emite coordenadas en píxeles del recorte ampliado: las reducimos a píxeles de la ilustración
    return f'<g transform="scale({1/s:.5f})">{svg_body}</g>'


def clean_mask(m):
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    nc, cc, st, _ = cv2.connectedComponentsWithStats(m)
    if nc <= 1: return m
    big = st[1:, cv2.CC_STAT_AREA].max(); keep = np.zeros_like(m)
    for j in range(1, nc):
        if st[j, cv2.CC_STAT_AREA] > big * 0.008: keep[cc == j] = 1
    return binary_fill_holes(keep).astype(np.uint8)


def region(rgb, mask, box, ink_thr=70, clahe=False, ink_only_dark=None):
    """Devuelve (rellenos, líneas, contorno) de una región, en coordenadas de la ilustración relativas a box."""
    x0, y0, x1, y1 = box
    crop = rgb[y0:y1, x0:x1].copy(); mc = mask[y0:y1, x0:x1]
    crop = cv2.resize(crop, None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC)
    mc = cv2.resize(mc * 255, None, fx=S, fy=S, interpolation=cv2.INTER_LINEAR)
    mc = (cv2.GaussianBlur(mc, (3, 3), 0) > 127).astype(np.uint8)
    if clahe:
        l = cv2.cvtColor(crop, cv2.COLOR_RGB2LAB)
        l[:, :, 0] = cv2.createCLAHE(clipLimit=2.4, tileGridSize=(8, 8)).apply(l[:, :, 0])
        crop = cv2.cvtColor(l, cv2.COLOR_LAB2RGB)
    flat = cv2.bilateralFilter(crop, 9, 40, 9)
    flat[mc == 0] = KEY
    fill = body(trace(flat, colormode='color', hierarchical='stacked', mode='spline', **FILL))
    # quita el fondo (color clave y el rectángulo inicial si vtracer lo fusionó)
    fill = re.sub(r'<path[^>]*fill="#[Ff][A-Fa-f0-9]0[0-9A-Fa-f][Ff][A-Fa-f0-9]"[^>]*/>', '', fill)
    g = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
    thr = ink_only_dark if ink_only_dark else ink_thr
    ink = ((g < thr) & (mc > 0)).astype(np.uint8)
    ink = cv2.morphologyEx(ink, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    im2 = np.full((*ink.shape, 3), 255, np.uint8); im2[ink > 0] = 0
    lines = body(trace(im2, colormode='binary', mode='spline', **LINE))
    # contorno para recortar (clipPath)
    im3 = np.full((*mc.shape, 3), 255, np.uint8); im3[mc > 0] = 0
    outline = body(trace(im3, colormode='binary', mode='polygon', filter_speckle=20, path_precision=1))
    to_d = lambda b: ' '.join(re.findall(r'd="([^"]+)"', b))
    # fusiona el contorno en un único path con su translate
    outl = ''.join(f'<path d="{d}" transform="{t}"/>' for d, t in re.findall(r'd="([^"]+)"[^>]*?transform="([^"]+)"', outline)) or outline
    return scale_paths(fill, S), scale_paths(lines, S), scale_paths(outl, S)


def bbox(m, pad=4):
    ys, xs = np.where(m > 0)
    return [int(xs.min() - pad), int(ys.min() - pad), int(xs.max() + pad + 1), int(ys.max() + pad + 1)]


def main(n):
    i = NAMES.index(n) + 1
    m = clean_mask(((lab == i) & (fga > 120)).astype(np.uint8))
    box = bbox(m)
    out = dict(name=n, box=box, parts={})
    rgb = src0.copy()
    if n == 'dog':
        hsv = cv2.cvtColor(src0, cv2.COLOR_RGB2HSV)
        tongue = ((hsv[:, :, 1] > 90) & (hsv[:, :, 2] > 120) & ((hsv[:, :, 0] < 12) | (hsv[:, :, 0] > 165))).astype(np.uint8)
        tongue[:788, :] = 0; tongue[840:, :] = 0; tongue[:, :705] = 0; tongue[:, 765:] = 0
        tongue = clean_mask(cv2.dilate(tongue, np.ones((3, 3), np.uint8))) & m
        neck = 842
        head = m.copy(); head[neck:, :] = 0
        # base: cuerpo con la cabeza rellena de pelo liso (así al inclinar la cabeza no se duplica)
        out['parts']['body'] = region(rgb, m, box, clahe=True, ink_only_dark=34)
        tb = bbox(tongue, 2)
        out['parts']['tongue'] = region(rgb, tongue, tb) + (tb,)
    else:
        out['parts']['body'] = region(rgb, m, box)
    json.dump(out, open(f'/tmp/m/vec/{n}.json', 'w'))
    size = sum(len(''.join(p[:3])) for p in out['parts'].values())
    print(n, box, size // 1024, 'KB')


if __name__ == '__main__':
    main(sys.argv[1])
