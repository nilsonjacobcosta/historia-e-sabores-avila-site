import json,re,pathlib
R=pathlib.Path('/home/claude/historia-e-sabores-avila-site')
O=R/'src/dados-orig'; D=R/'dados'
L=lambda n:json.load(open(O/(n+'.json')))
def drop(o):
    if isinstance(o,dict): return {k:drop(v) for k,v in o.items() if k not in('ficha','caminho_origem')}
    if isinstance(o,list): return [drop(x) for x in o]
    return o
P=L('pessoas');I=L('imagens');REL=L('relacoes');REC=L('receitas');LUG=L('lugares');T=L('linha_do_tempo')
UNFLAG_P={'juvenal'}
for p in P:
    if p['id'] in UNFLAG_P: p['possivelmente_vivo']=False
vivos={p['id'] for p in P if p.get('possivelmente_vivo')}
KEY=['Maria Amâncio','Antonieta','Zaida','Lacir','Joaquina Rita','Ivone','Walter','Walma','Dinor']
for p in P:
    if p['id'] in vivos:
        if p['id']=='fabricio-de-avila-ferreira': p['resumo']='Autor do livro "Avila: 300 anos de História & Sabores" (2009).'
        elif p['id']=='angelo-davila': p['resumo']='Cronista citado no livro.'
        else: p['resumo']='Autor(a) de receita(s) do livro.' if p.get('receitas') else 'Citado(a) no livro.'
        for k in('nascimento','morte','lugar','conjuge','foto','nascimento_detalhe','morte_detalhe','nota_confirmar'): p[k]=None
        p['conjuges']=[];p['divergencias']=[]
    else:
        parts=re.split(r'(?<=[.;])\s+',p.get('resumo') or '')
        p['resumo']=' '.join(x for x in parts if not any(k in x for k in KEY)) or 'Citado(a) no livro.'
        if p.get('conjuge') in vivos: p['conjuge']=None
        p['conjuges']=[c for c in p.get('conjuges',[]) if c not in vivos]
        if p.get('nota_confirmar') and any(k in p['nota_confirmar'] for k in KEY): p['nota_confirmar']=None
EXTRA=('vid-lanc-30','ig-20201117-132529-f1','ig-20201117-132529-f3','livro-p125-106','ig-20210125-132044-f2')
fl={f['id'] for f in REL['fotos'] if f.get('contem_possivelmente_vivos')}
fl={x for x in fl if not x.startswith('livro-p085-064')}
for i in I:
    if i['id'].startswith(EXTRA): fl.add(i['id'])
n=0
for i in I:
    i['possivelmente_vivos']=i['id'] in fl
    if i['possivelmente_vivos']:
        n+=1;i['legenda_curta']='Foto de família'+(' ('+str(i['data'])[:4]+')' if i.get('data') else '')
        i['alt']='Foto de família; identificação das pessoas reservada.';i['pessoas_citadas']=[];i.pop('nota',None)
for f in REL['fotos']:
    if f['id'] in fl: f['pessoas_ids']=[];f['contem_possivelmente_vivos']=True
    else: f['contem_possivelmente_vivos']=False
REL['arestas']=[a for a in REL['arestas'] if not(a.get('tipo')=='conjuge' and(a['de'] in vivos or a['para'] in vivos))]
for e in T: e['pessoas_ids']=[x for x in e.get('pessoas_ids',[]) if x not in vivos]
for name,obj in [('pessoas',P),('imagens',I),('relacoes',REL),('receitas',REC),('lugares',LUG),('linha_do_tempo',T)]:
    json.dump(drop(obj),open(D/(name+'.json'),'w'),ensure_ascii=False,separators=(',',':'))
print('fotos ocultas',n,'vivos',len(vivos))
