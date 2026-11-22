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
mapa=re.sub(r'(<desc id="mapa-d">).*?(</desc>)',r'\1Mapa estilizado, fora de escala. O traçado azul é um esquema geral que liga a Ilha do Pico, Borda do Campo e Barbacena, São Domingos do Araxá, Morro Alto e Goiás; não é o caminho de uma única família. Brasília aparece como ponto de contexto de hoje.\2',mapa,flags=re.S)
mapa=mapa.replace('Brasília, onde Nilson e Duda moram hoje','Brasília, ponto de contexto de hoje')
out=t.replace('{{CSS}}',css).replace('{{SPRITE}}',m.group(0)).replace('{{MAPA}}',mapa)
(r/'index.html').write_text(out)
print(len(out))
