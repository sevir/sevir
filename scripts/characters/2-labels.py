"""Reparte la silueta de la familia (rembg) entre personajes: semillas SAM + watershed.
Genera labels.npy (1=dad 2=mom 3=kidA 4=kidB 5=dog). Ver README.md de esta carpeta."""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage
src = cv2.imread('src.png'); fga = np.array(Image.open('fg.png'))[:, :, 3]
H, W = fga.shape
names = ['dad', 'mom', 'kidA', 'kidB', 'dog']
seeds = {
 'kidA': [(560,420),(520,500),(480,500),(590,620),(570,760),(540,800),(600,800),(620,780),(560,820),(540,900),(600,940),(520,990),(620,500)],
 'kidB': [(900,600),(860,610),(880,800),(880,880),(866,945),(932,945),(850,990),(950,990),(900,700),(868,925),(935,925)],
 'mom':  [(840,140),(960,200),(970,300),(900,500),(980,600),(830,600),(1000,450),(1020,400),(880,300),(820,700),(800,650),(985,700)],
 'dad':  [(620,400),(720,450),(560,450),(680,650),(700,750),(670,150),(600,300),(760,330),(650,900),(655,960)],
 'dog':  [(720,800),(660,720),(800,720),(700,950),(740,880)]}
markers = np.zeros((H, W), np.int32); markers[fga < 10] = 6
for i, n in enumerate(names):
    m = cv2.erode((np.array(Image.open(f'mask_{n}.png')) > 127).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    markers[m & (fga > 128)] = i + 1
for n, li in (('teddy', 3), ('plush', 4)):
    m = np.array(Image.open(f'mask_{n}.png')) > 127
    markers[cv2.erode(m.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = li
for i, n in enumerate(names):
    for (x, y) in seeds[n]: cv2.circle(markers, (x, y), 7, i + 1, -1)
ws = cv2.watershed(cv2.GaussianBlur(src, (3, 3), 0), markers.copy())
b = ws == -1; lab = ws.copy(); lab[b] = 0
lab = np.where(b, cv2.dilate(lab.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.int32), lab)
todo = (fga > 40) & ((lab == 6) | (lab <= 0)); known = (lab >= 1) & (lab <= 5)
_, idx = ndimage.distance_transform_edt(~known, return_indices=True)
lab[todo] = lab[idx[0], idx[1]][todo]
np.save('labels.npy', lab)
