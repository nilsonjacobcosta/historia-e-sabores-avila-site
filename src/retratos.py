#!/usr/bin/env python3
"""Recorta retratos 4:5 centrados no rosto de cada pessoa (img/ret-<id>.webp) e grava `retrato` em src/dados-orig/pessoas.json.
Pessoas com foto de grupo ou sem rosto identificável (casa, grupo de irmãos, dois retratos de pessoas diferentes) ficam sem recorte
e aparecem com monograma no cartão; a foto continua na galeria. Idempotente."""
import json, pathlib
from PIL import Image
R = pathlib.Path('/home/claude/historia-e-sabores-avila-site')
P = json.load(open(R/'src/dados-orig/pessoas.json'))
I = {i['id']: i for i in json.load(open(R/'src/dados-orig/imagens.json'))}
# id da pessoa: (cx, cy, h)  fracoes da largura/altura da imagem; h = altura do recorte / altura da imagem
S = {
 'tiburcio-joaquim-de-avila':(.25,.5,.88),'thereza-thomazia-teixeira':(.75,.5,.88),
 'joaquim-esteves-de-avila':(.25,.5,.88),'joaquina-candida-da-conceicao':(.75,.5,.88),
 'adelia-benevides-jacob':(.75,.5,.88),
 'carlos-de-avila-netto-carico':(.25,.5,.88),'irinea-de-aguiar-avila':(.75,.5,.88),
 'mariana-de-avila-fiica':(.25,.5,.88),'jose-porfirio-ferreira-juquinha':(.75,.5,.88),
 'francisco-antonio-de-avila-pentavo':(.51,.43,.62),'manoel-francisco-de-avila':(.49,.45,.6),
 'cassiano-barbosa-de-affonseca-e-silva':(.46,.3,.62),
 'hipolita-cassiana-lemos':(.27,.14,.3),'manoel-esteves-de-avila':(.64,.125,.3),
 'joaquim-antonio-de-avila-zico':(.5,0.28,.41),'manoel-antonio-de-avila-lico':(.5,0.29,.41),
 'jose-antonio-de-avila':(.5,0.29,.41),'alcides-joaquim-de-avila':(.5,0.30,.41),
 'maria-candida-da-conceicao-nica':(.5,0.34,.41),'ana-candida-de-avila-donana':(.5,0.30,.41),
 'antonio-joaquim-de-avila-tonico':(.5,0.31,.41),'agenor-joaquim-de-avila':(.5,0.30,.41),
 'adhemar-antonio-de-avila':(.5,0.28,.41),'jose-de-avila-juca':(.5,0.31,.41),
 'renato-benevides-de-avila':(.5,.3,.5),
 'joaquim-de-avila-aviador':(.32,.3,.62),
 'sa-jeronima':(.40,.19,.45),'mariquinha':(.5,.18,.5),'francisco-amancio-da-costa':(.46,.22,.5),
}
out = pathlib.Path(R/'img'); n = 0
for p in P:
    p.pop('retrato', None)
    s = S.get(p['id']); f = p.get('foto')
    if not s or not f: continue
    im = Image.open(R/I[f]['arquivo']).convert('RGB'); W, H = im.size
    cx, cy, h = s
    ch = h*H; cw = .8*ch
    if cw > W: cw = W; ch = cw/.8
    x0 = min(max(cx*W-cw/2, 0), W-cw); y0 = min(max(cy*H-ch/2, 0), H-ch)
    c = im.crop((int(x0), int(y0), int(x0+cw), int(y0+ch))).resize((192, 240), Image.LANCZOS)
    name = 'img/ret-%s.webp' % p['id']
    c.save(R/name, 'WEBP', quality=82); p['retrato'] = name; n += 1
json.dump(P, open(R/'src/dados-orig/pessoas.json','w'), ensure_ascii=False, indent=1)
print('retratos', n)
