import sys, json, numpy as np
from PIL import Image
from rembg import new_session, remove
k=sys.argv[1]; pts=json.loads(sys.argv[2]); neg=json.loads(sys.argv[3]) if len(sys.argv)>3 else []
im=Image.open('src.png').convert('RGB')
pr=[{"type":"point","data":p,"label":1} for p in pts]+[{"type":"point","data":p,"label":0} for p in neg]
out=remove(im,session=new_session('sam'),sam_prompt=pr,only_mask=True)
a=np.array(out); print(k,(a>127).mean(),flush=True); Image.fromarray(a).save(f'mask_{k}.png')
