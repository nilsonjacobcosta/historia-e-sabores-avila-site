# Correções do juiz de conteúdo (22/11). Aplica sobre src/dados-orig/ (idempotente).
import json,pathlib
O=pathlib.Path('/home/claude/historia-e-sabores-avila-site/src/dados-orig')
L=lambda n:json.load(open(O/(n+'.json')))
S=lambda n,o:json.dump(o,open(O/(n+'.json'),'w'),ensure_ascii=False,indent=1)
P=L('pessoas');I=L('imagens');R=L('relacoes');T=L('linha_do_tempo');LU=L('lugares')
pid={p['id']:p for p in P}
pid['tiburcio-de-avila-menino']['resumo']='Filho de Marianno, falecido aos oito anos. Carlos deu o nome Tibúrcio a dois filhos (Tibúrcio Joaquim e Tibúrcio Germano) em homenagem a este irmão.'
c=pid['carlos-joaquim-de-avila'];c['conjuges']=[x for x in c['conjuges'] if x!='carlota-ana-dabadia']
if c.get('morte_detalhe'): c['morte_detalhe']['nota']='Data da morte não informada no livro.'
pid['carlota-ana-dabadia']['conjuge']=None;pid['carlota-ana-dabadia']['conjuges']=[]
NP='O livro traz o sobrenome Portella na ascendência direta de Tibúrcio Joaquim. A família ainda não confirmou se esta linha chega ao Nilson; por isso ela aparece só por constar no livro.'
for k in ['nicolao-alves-portella-de-oliveira','maria-do-carmo-de-oliveira','ana-candida-de-oliveira','ana-rosa-de-jesus']:
    pid[k]['aconfirmar']=True;pid[k]['nota_confirmar']=NP
i=pid['irinea-de-aguiar-avila'];i['resumo']=i['resumo'].replace('A ascendência dela (Ferreira de Aguiar/Portella) pertence a ramo arquivado e não é detalhada aqui.','A ascendência dela (família Ferreira de Aguiar) não é detalhada aqui.');i['nota_confirmar']=None
pid['marianna-joaquina-das-neves']['nascimento']='bat. 1754'
pid['joaquim-de-avila-aviador']['morte']='c. 1965/66 (inferido)'
pid['francisca-da-conceicao']['morte']='c. 1756 (inferido)'
pid['maria-rita-de-paiva']['resumo']='Esposa de Chico do Muro; o livro a chama de Paiva por casamento.'
x=pid['ana-candida-candinha'];x['resumo']=x['resumo'].replace('nem com a "Vovó Candinha" (Cândida Umbelina), de ramo arquivado.','nem com outras Candinhas citadas no livro.')
x=pid['antonio-de-avila-sinho'];x['resumo']=x['resumo'].replace(' (a família de sua esposa pertence ao ramo arquivado)','')
pid['antonio-joaquim-de-avila']['nota_confirmar']='Sesmaria "Pederneiras" e cotas do testamento a confirmar. Há homônimos: o filho de Francisco Antonio e "Tonico".'
pid['marianno-joaquim-de-avila']['foto']=None;pid['carlos-joaquim-de-avila']['foto']=None
pid['renato-benevides-de-avila']['resumo']=pid['renato-benevides-de-avila']['resumo'].replace('no colo da mãe na foto','na foto')
R['arestas']=[a for a in R['arestas'] if not(a.get('tipo')=='conjuge' and 'carlota-ana-dabadia' in (a['de'],a['para']))
 and not(a.get('tipo')=='pessoa_foto' and a['de']=='tiburcio-de-avila-menino' and a['para'].startswith('livro-p111-088'))
 and not(a.get('tipo')=='pessoa_foto' and a['de']=='mariana-de-avila-fiica' and a['para'].startswith('ig-20210530-131506'))]
for f in I:
    if f['id']=='ig-20201117-132529-f1': f['legenda_curta']='Casa de fazenda (foto colorida), em postagem sobre a culinária do Morro Alto';f['alt']='Casa de fazenda térrea de paredes claras, com cerca e terreiro.'
    if f['id']=='ig-20201117-132529-f2': f['legenda_curta']='Casas de fazenda (foto colorida), em postagem sobre a culinária do Morro Alto';f['alt']='Casa de fazenda térrea e telheiro, com vegetação ao fundo.'
    if f['id']=='ig-20201117-132529-f3': f['legenda_curta']='Foto de estúdio da família de Joaquim Antonio e Adélia (1927/28)';f['alt']='Fotografia de estúdio de grupo familiar.'
    if f['id'].startswith('livro-p109-086'): f['legenda_curta']='Registro de família manuscrito, com nascimentos e batismos; Carlos Joaquim e Mariana de Paula Carneiro constam como padrinhos'
    if f['id'].startswith('livro-p113-091'): f['alt']='Fotografia de estúdio de grupo familiar, com mulher idosa sentada ao centro.'
for e in T:
    if e['id']=='ev-42': e['texto']='06/12/1956; ensinou Renato (filho de Zico) e Fiíca.'
    if e['id']=='ev-13' and e['nivel']=='controverso': e['nivel']='P';e['nota']=((e.get('nota') or '')+' Só o livro traz esta informação.').strip()
for l in LU:
    if l['id']=='goias': l['descricao']=l['descricao'].replace('pesquisa/verificacao','pesquisa de contexto')
    if l['id']=='araxa' and l.get('coordenadas_nota'): l['coordenadas_nota']=l['coordenadas_nota'].replace('pt.wikipedia','link iPatrimônio dentro da pt.wikipedia') if 'iPatrim' not in l['coordenadas_nota'] else l['coordenadas_nota']
for n,o in [('pessoas',P),('imagens',I),('relacoes',R),('linha_do_tempo',T),('lugares',LU)]: S(n,o)
print('ok')
