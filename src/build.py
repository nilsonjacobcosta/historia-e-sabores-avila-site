import re,pathlib
r=pathlib.Path('/home/claude/historia-e-sabores-avila-site')
t=(r/'src/template.html').read_text()
css=(r/'design/base.css').read_text()
orn=(r/'design/ornamentos.svg.html').read_text()
m=re.search(r'<svg class="sprite" xmlns.*?</svg>',orn,re.S)
mapa=(r/'design/mapa.svg').read_text()
mapa=mapa[mapa.index('<svg'):]
assert "svg.classList.add('espera');" in mapa
mapa=mapa.replace("svg.classList.add('espera');","svg.classList.add('anima');")
assert m
out=t.replace('{{CSS}}',css).replace('{{SPRITE}}',m.group(0)).replace('{{MAPA}}',mapa)
(r/'index.html').write_text(out)
print(len(out))
