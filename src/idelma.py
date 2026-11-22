# Acrescenta as postagens de @idelmadacosta2 e as linhas Costa/Jacob (22/11, noite). Idempotente; roda depois de corrige.py.
import json,pathlib,re,glob,os
from PIL import Image
RT=pathlib.Path('/home/claude/historia-e-sabores-avila-site');O=RT/'src/dados-orig'
AC=pathlib.Path('/home/claude/historia-e-sabores-avila/fontes-integrais/instagram-idelma/postagens')
L=lambda n:json.load(open(O/(n+'.json')));S=lambda n,o:json.dump(o,open(O/(n+'.json'),'w'),ensure_ascii=False,indent=1)
P=L('pessoas');I=L('imagens');R=L('relacoes');T=L('linha_do_tempo')
NEW_P={'francisco-amancio-da-costa','virgilina-rosa-de-jesus','joaquim-manoel-da-costa','maria-rosa-de-sao-jose','manoel-gomes-de-menezes','maria-roza-gomes','manoel-amancio-da-costa','zilda-jacob-da-costa','hilmovir-jacob-de-rezende','ilmovir-jose-da-costa','nilson-jacob-da-costa'}
P=[p for p in P if p['id'] not in NEW_P]
I=[i for i in I if not i['id'].startswith('ig-idelma-')]
R['fotos']=[f for f in R['fotos'] if not f['id'].startswith('ig-idelma-')]
R['arestas']=[a for a in R['arestas'] if not(str(a.get('de','')).startswith('ig-idelma-') or str(a.get('para','')).startswith('ig-idelma-') or a.get('de') in NEW_P or a.get('para') in NEW_P)]
T=[e for e in T if e['id']!='ev-idelma-01']
pid={p['id']:p for p in P}
F1={'francisco-amancio-da-costa-e-virgilina':'francisco-amancio-da-costa-e-virgilina'}
MAP={ # slug: (pessoas_ids, lugar_id, vinculo)
'retrato-casal-pb':([],None,'Sem vínculo'),'grupo-idosos-colorido':([],None,'Sem vínculo'),'casal-idosos-sentados':([],None,'Sem vínculo'),
'bodas-de-ouro-francisco-amancio-virgilina':(['francisco-amancio-da-costa','virgilina-rosa-de-jesus'],'araxa','Provável'),
'francisco-amancio-da-costa-e-virgilina':(['francisco-amancio-da-costa','virgilina-rosa-de-jesus'],'araxa','Provável'),
'maria-custodia-e-joao-jacob':(['joao-jacob','maria-custodia-de-oliveira-naves','adelia-benevides-jacob'],None,'Confirmado'),
'capa-reminiscencias-do-morro-alto':([],'morro-alto','Hipótese'),
'familia-grande-pb-anos-70':([],None,'Provável'),
'maria-candida-da-conceicao-nica':(['maria-candida-da-conceicao-nica'],'ibia','Confirmado'),
'chernovitz-e-medicina-popular':(['joaquim-esteves-de-avila','joaquina-candida-da-conceicao'],'araxa','Confirmado'),
'joaquim-esteves-de-avila-e-joaquina':(['joaquim-esteves-de-avila','joaquina-candida-da-conceicao'],'morro-alto','Confirmado'),
'casa-santa-casa-misericordia-araxa':(['manoel-francisco-de-avila'],'santa-casa-araxa','Confirmado'),
'manoel-francisco-de-avila':(['manoel-francisco-de-avila'],'araxa','Confirmado'),
'francisco-antonio-de-avila':(['francisco-antonio-de-avila-pentavo','ana-rosa-de-jesus'],None,'Confirmado'),
'morro-alto-acores-e-minas':([],'morro-alto','Confirmado'),
'antonio-joaquim-de-avila':(['antonio-joaquim-de-avila'],None,'Confirmado'),
'joao-de-avila-da-silveira':(['joao-de-avila-da-silveira'],'pico','Confirmado'),
'joao-de-avila-da-silveira-geneaminas':(['joao-de-avila-da-silveira','francisca-da-conceicao'],'borda-do-campo','Confirmado'),
'erupcao-1748-emigracao-pico':(['joao-de-avila-da-silveira','francisca-da-conceicao'],'pico','Confirmado'),
'da-ilha-do-pico-aos-sertoes-das-gerais':([],'pico','Confirmado'),
'capitao-joao-de-avila-raposo-geneaminas':(['joao-de-avila-raposo','maria-do-rosario'],'pico','Confirmado'),
'brasao-joao-de-avila-raposo':(['joao-de-avila-raposo'],'angra','Confirmado')}
NOME={p['id']:p['nome'] for p in P}
first={}
for d in sorted(os.listdir(AC)):
    slug=d.split('_idelmadacosta2_')[1]; ids,lug,vin=MAP[slug]
    ft=open(AC/d/'ficha.md').read()
    desc=dict(re.findall(r'- Imagem (\d+): (.+)',ft))
    leg=re.search(r'## O que a legenda diz.*?\n(.+?)\n\n',ft,re.S).group(1).strip()
    ciclo=sorted(glob.glob(str(AC/d/'foto-*.jpg')))
    data=d[:10]
    for n,fp in enumerate(ciclo,1):
        fid=f"ig-idelma-{d[:10].replace('-','')}-{d[11:15]}-{slug[:24]}-f{n}"
        im=Image.open(fp).convert('RGB');im.thumbnail((1100,1100))
        im.save(RT/'img'/f'{fid}.webp','WEBP',quality=80)
        if n==1: first[slug]=fid
        short=(leg if leg!='Sem legenda.' else d.split('_idelmadacosta2_')[1].replace('-',' ').capitalize())[:150]
        I.append({'id':fid,'arquivo':f'img/{fid}.webp','mini':f'img/{fid}.webp','largura':im.size[0],'altura':im.size[1],'origem':'instagram','credito':'@idelmadacosta2 (Idelma Borges Costa)','data':data,'data_tipo':'postagem','legenda_curta':short,'alt':desc.get(str(n),short),'pessoas_citadas':[NOME.get(i,i) for i in ids],'lugar':None,'nivel_evidencia':'D','vinculo':vin,'nota':'Captura de tela; comentários de terceiros não coletados.'})
        R['fotos'].append({'id':fid,'arquivo':f'img/{fid}.webp','lugar_id':lug,'pessoas_ids':ids,'contem_possivelmente_vivos':False,'sugestao_exibicao':'livre dentro do acervo familiar privado','nivel_evidencia':'D'})
        for i in ids: R['arestas'].append({'tipo':'pessoa_foto','de':i,'para':fid})
        if lug: R['arestas'].append({'tipo':'foto_lugar','de':fid,'para':lug})
def mk(id,nome,**k):
    b={'id':id,'nome':nome,'nascimento':None,'morte':None,'lugar':None,'ramo':'minas','evidencia':'D','aconfirmar':True,'pais':[],'conjuge':None,'filhos':[],'foto':None,'resumo':'','linha':'costa','apelidos':[],'conjuges':[],'nascimento_detalhe':None,'morte_detalhe':None,'receitas':[],'fontes':[{'arquivo':'fontes-integrais/instagram-idelma/INDICE.md'}],'evidencia_detalhe':'Legenda de @idelmadacosta2 (D).','encontrado_por_este_estudo':False,'possivelmente_vivo':False,'divergencias':[],'nota_confirmar':None}
    b.update(k);return b
fc=first['francisco-amancio-da-costa-e-virgilina']
NOTA='Confirmado pelo Nilson em 22/11/2026: o avô paterno Manoel Amâncio da Costa «Sorriso» é filho de Francisco Amâncio da Costa e Virgilina Rosa de Jesus. Sem documento ainda; o livro (pp. 42–43) e e-mails de 2013 são coerentes.'
P+= [
mk('joaquim-manoel-da-costa','Joaquim Manoel da Costa',filhos=['francisco-amancio-da-costa'],conjuge='maria-rosa-de-sao-jose',conjuges=['maria-rosa-de-sao-jose'],resumo='Pai de Francisco Amâncio da Costa (legenda de @idelmadacosta2).',lugar=None),
mk('maria-rosa-de-sao-jose','Maria Rosa de São José',filhos=['francisco-amancio-da-costa'],conjuge='joaquim-manoel-da-costa',conjuges=['joaquim-manoel-da-costa'],resumo='Mãe de Francisco Amâncio da Costa (legenda de @idelmadacosta2).'),
mk('manoel-gomes-de-menezes','Manoel Gomes de Menezes',filhos=['virgilina-rosa-de-jesus'],conjuge='maria-roza-gomes',conjuges=['maria-roza-gomes'],resumo='Pai de Virgilina Rosa de Jesus. Possível ligação com Joaquim Gomes de Menezes, que casou com Maria, filha de Antonio Joaquim de Avila: a confirmar.'),
mk('maria-roza-gomes','Maria Roza Gomes',filhos=['virgilina-rosa-de-jesus'],conjuge='manoel-gomes-de-menezes',conjuges=['manoel-gomes-de-menezes'],resumo='Mãe de Virgilina Rosa de Jesus.'),
mk('virgilina-rosa-de-jesus','Virgilina Rosa de Jesus ("Vovó Virgilina")',pais=['manoel-gomes-de-menezes','maria-roza-gomes'],conjuge='francisco-amancio-da-costa',conjuges=['francisco-amancio-da-costa'],lugar='araxa',filhos=['manoel-amancio-da-costa'],resumo='Casou-se com Francisco Amâncio da Costa em 1900; bodas de ouro em setembro de 1950, em Araxá (folheto da família; o dia está ilegível na foto). Filha de Manoel Gomes de Menezes e Maria Roza Gomes.',evidencia='P',nota_confirmar=NOTA,evidencia_detalhe='Livro (pp. 42–43) e postagens de @idelmadacosta2 (D).'),
mk('francisco-amancio-da-costa','Francisco Amâncio da Costa ("Vovô Chico")',pais=['joaquim-manoel-da-costa','maria-rosa-de-sao-jose'],conjuge='virgilina-rosa-de-jesus',conjuges=['virgilina-rosa-de-jesus'],lugar='araxa',filhos=['manoel-amancio-da-costa'],foto=fc,resumo='Filho de Joaquim Manoel da Costa e Maria Rosa de São José; casado com Virgilina Rosa de Jesus; morava em Araxá (Rua Olegário Maciel, 603). O livro explica que «Amâncio» era nome e passou a ser usado como sobrenome nos filhos homens. É bisavô do Nilson e avô do pai dele (confirmado pelo Nilson).',evidencia='P',nota_confirmar=NOTA,evidencia_detalhe='Livro (pp. 42–43) e postagens de @idelmadacosta2 (D).'),
mk('manoel-amancio-da-costa','Manoel Amâncio da Costa ("Sorriso")',pais=['francisco-amancio-da-costa','virgilina-rosa-de-jesus'],conjuge='zilda-jacob-da-costa',conjuges=['zilda-jacob-da-costa'],filhos=['ilmovir-jose-da-costa'],resumo='Avô paterno do Nilson; irmão de Joaquim Amâncio da Costa (casado com Cândida). É o «Tio Manoel, Manoel Sorriso» do livro, filho de Francisco Amâncio da Costa e Virgilina (confirmado pelo Nilson).',evidencia='P',nota_confirmar=NOTA,evidencia_detalhe='E-mail «Família Costa» (2013) e árvore do Nilson (pesquisa/); filiação confirmada pelo Nilson.',fontes=[{'arquivo':'pesquisa/arvore-genealogica-nilson.md'}]),
mk('hilmovir-jacob-de-rezende','Ilmovir (Hilmovir) Jacob de Rezende ("Vitinho")',pais=['joao-jacob','maria-custodia-de-oliveira-naves'],conjuge='maria-candida-da-conceicao-nica',conjuges=['maria-candida-da-conceicao-nica'],lugar='ibia',filhos=['zilda-jacob-da-costa','zaida-jacob'],linha='jacob-naves',resumo='Casou-se com Maria Cândida (Nica); morava em Ibiá. O livro lista um Ilmovir Jacob de Rezende entre os 16 filhos de João Jacob e Maria Custódia, e a legenda de @idelmadacosta2 chama os dois de bisavós do pai dela; o Nilson confirmou que os pais dele eram primos pela linha Jacob. Pai de Zaida e de Zilda.',evidencia='P',evidencia_detalhe='Livro e legendas de @idelmadacosta2 (D).',fontes=[{'arquivo':'pesquisa/arvore-genealogica-nilson.md'}]),
mk('zilda-jacob-da-costa','Zilda Jacob da Costa',pais=['hilmovir-jacob-de-rezende','maria-candida-da-conceicao-nica'],conjuge='manoel-amancio-da-costa',conjuges=['manoel-amancio-da-costa'],filhos=['ilmovir-jose-da-costa'],linha='jacob-naves',resumo='Avó paterna do Nilson (também «Zilda Jacob de Ávila»); irmã de Zaida Jacob; filha de Nica. É a ponte entre o Nilson e os Avila do livro.',evidencia='D',nota_confirmar='Falta certidão que ligue Zilda a Nica e Hilmovir; hoje apoiam: confirmação do Nilson e legenda da Idelma.',fontes=[{'arquivo':'pesquisa/arvore-genealogica-nilson.md'}]),
mk('ilmovir-jose-da-costa','Ilmovir José da Costa',pais=['manoel-amancio-da-costa','zilda-jacob-da-costa'],filhos=['nilson-jacob-da-costa'],morte='26/01/2015',resumo='Pai do Nilson.',evidencia='B',aconfirmar=False,evidencia_detalhe='Minuta do termo de cessão de direitos hereditários (2022) e e-mail de 2013.',fontes=[{'arquivo':'pesquisa/arvore-genealogica-nilson.md'}]),
mk('nilson-jacob-da-costa','Nilson Jacob da Costa',pais=['ilmovir-jose-da-costa'],resumo='Neto de Zilda Jacob da Costa e Manoel Amâncio da Costa; bisneto de Maria Cândida (Nica). Autor deste acervo.',evidencia='B',aconfirmar=False,possivelmente_vivo=True,evidencia_detalhe='Informação do próprio Nilson.',fontes=[{'arquivo':'pesquisa/arvore-genealogica-nilson.md'}]),
]
pid={p['id']:p for p in P}
n=pid['maria-candida-da-conceicao-nica'];n['filhos']=['zaida-jacob','zilda-jacob-da-costa'];n['conjuge']='hilmovir-jacob-de-rezende';n['conjuges']=['hilmovir-jacob-de-rezende']
for k_ in ('francisco-amancio-da-costa','virgilina-rosa-de-jesus','manoel-amancio-da-costa'): pid_=None
pid['zaida-jacob']['pais']=['maria-candida-da-conceicao-nica','hilmovir-jacob-de-rezende']
for k in ('joao-jacob','maria-custodia-de-oliveira-naves'):
    pid[k]['filhos']=list(dict.fromkeys(pid[k]['filhos']+['hilmovir-jacob-de-rezende']))
# Portella: Ana Rosa de Jesus consta como pentavó na árvore do Nilson
a=pid['ana-rosa-de-jesus'];a['nota_confirmar']='Consta como pentavó na árvore do Nilson (pesquisa/arvore-genealogica-nilson.md), pelo livro: esposa de Francisco Antonio de Avila. Os pais dela (Nicolao Alves Portella e Maria Josefa Rodrigues de Oliveira) vêm só do livro e de uma legenda da Idelma.'
for p in P:
    if p['id'] in ('francisco-antonio-de-avila-pentavo',): p['nota_confirmar']=(p.get('nota_confirmar') or '')
for pid_ in NEW_P-{'francisco-amancio-da-costa'}: pass
for a_ in [('francisco-amancio-da-costa','genitor_de','manoel-amancio-da-costa'),('virgilina-rosa-de-jesus','genitor_de','manoel-amancio-da-costa'),('joaquim-manoel-da-costa','genitor_de','francisco-amancio-da-costa'),('maria-rosa-de-sao-jose','genitor_de','francisco-amancio-da-costa'),('manoel-gomes-de-menezes','genitor_de','virgilina-rosa-de-jesus'),('maria-roza-gomes','genitor_de','virgilina-rosa-de-jesus'),('manoel-amancio-da-costa','genitor_de','ilmovir-jose-da-costa'),('zilda-jacob-da-costa','genitor_de','ilmovir-jose-da-costa'),('ilmovir-jose-da-costa','genitor_de','nilson-jacob-da-costa'),('hilmovir-jacob-de-rezende','genitor_de','zilda-jacob-da-costa'),('maria-candida-da-conceicao-nica','genitor_de','zilda-jacob-da-costa'),('hilmovir-jacob-de-rezende','genitor_de','zaida-jacob'),('joao-jacob','genitor_de','hilmovir-jacob-de-rezende'),('maria-custodia-de-oliveira-naves','genitor_de','hilmovir-jacob-de-rezende'),('francisco-amancio-da-costa','conjuge','virgilina-rosa-de-jesus'),('manoel-amancio-da-costa','conjuge','zilda-jacob-da-costa'),('hilmovir-jacob-de-rezende','conjuge','maria-candida-da-conceicao-nica'),('joaquim-manoel-da-costa','conjuge','maria-rosa-de-sao-jose'),('manoel-gomes-de-menezes','conjuge','maria-roza-gomes')]:
    if not any(x.get('tipo')==a_[1] and x['de']==a_[0] and x['para']==a_[2] for x in R['arestas']): R['arestas'].append({'tipo':a_[1],'de':a_[0],'para':a_[2]})
for i in ('francisco-amancio-da-costa','virgilina-rosa-de-jesus'):
    R['arestas']+= [{'tipo':'pessoa_lugar','de':i,'para':'araxa'}]
T.append({'ano':1950,'data':'1950-09','titulo':'Bodas de ouro de Francisco Amâncio da Costa e Virgilina Rosa de Jesus','texto':'Folheto de lembrança das bodas de ouro (Araxá, casamento em 1900). Leitura da foto da postagem de @idelmadacosta2; conferir com o original.','lugar_id':'araxa','pessoas_ids':['francisco-amancio-da-costa','virgilina-rosa-de-jesus'],'nivel':'D','fonte':[{'arquivo':'fontes-integrais/instagram-idelma/INDICE.md'}],'nota':'Leitura da imagem.','id':'ev-idelma-01'})
for k,o in [('pessoas',P),('imagens',I),('relacoes',R),('linha_do_tempo',T)]: S(k,o)
for k_ in ('francisco-amancio-da-costa','virgilina-rosa-de-jesus','manoel-amancio-da-costa'): pid[k_]['aconfirmar']=False
print('idelma ok',len(P),len(I))
