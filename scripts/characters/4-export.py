import json, re
def flat_clip(o):
    m=re.match(r'<g transform="scale\(([0-9.]+)\)">(.*)</g>$',o.strip(),re.S)
    sc,inner=m.group(1),m.group(2)
    return re.sub(r'<path ([^>]*?)transform="([^"]+)"',lambda k:f'<path {k.group(1)}transform="scale({sc}) {k.group(2)}"',inner)

OUT='/home/claude/sevir.org/static/images/chars/'
CH={
 'dad': dict(neck=238, pivot=[668,238], skin='#fcb46e', eyes=[[652,156,21,29],[713,140,19,29]], head=[672,30]),
 'mom': dict(neck=285, pivot=[872,280], skin='#fdbd7b', eyes=[[826,206,15,25],[886,197,17,26]], head=[880,62]),
 'kidA':dict(neck=560, pivot=[592,560], skin='#fdb76f', eyes=[[570,520,16,19],[625,512,16,21]], head=[585,402]),
 'kidB':dict(neck=724, pivot=[898,724], skin='#fdba75', eyes=[[872,673,14,19],[926,673,15,20]], head=[905,566]),
 'dog': dict(neck=842, pivot=[738,842], skin='#252527', eyes=[[712,741,12,17],[752,741,11,17]], head=[740,676]),
}
data={}
for n,c in CH.items():
    r=json.load(open(f'vec/{n}.json')); x0,y0,x1,y1=r['box']; w,h=x1-x0,y1-y0
    fill,lines,outl=r['parts']['body'][:3]
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w} {h}" width="{w}" height="{h}">'
         f'<defs><clipPath id="c">{flat_clip(outl)}</clipPath></defs>'
         f'<g transform="translate({x0} {y0})"><g clip-path="url(#c)">{fill}</g>{lines}</g></svg>')
    svg=re.sub(r'\s+',' ',svg)
    open(OUT+f'{n}.svg','w').write(svg)
    if n=='dog':
        tf,tl,to,tb=r['parts']['tongue']
        tw,th=tb[2]-tb[0],tb[3]-tb[1]
        open(OUT+'dog-tongue.svg','w').write(re.sub(r'\s+',' ',f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{tb[0]} {tb[1]} {tw} {th}" width="{tw}" height="{th}"><defs><clipPath id="c">{flat_clip(to)}</clipPath></defs><g transform="translate({tb[0]} {tb[1]})"><g clip-path="url(#c)">{tf}</g></g></svg>'))
        c['tongue']=tb
    data[n]=dict(box=[x0,y0,w,h],**c)
    print(n,len(svg)//1024,'KB')
import yaml
open('/home/claude/sevir.org/data/chars.yaml','w').write('# Generado por scripts/characters-svg.py — cajas, cuello, ojos y cabeza en píxeles de la ilustración (1526×1031)\n'+yaml.safe_dump(data,default_flow_style=None,sort_keys=False))
