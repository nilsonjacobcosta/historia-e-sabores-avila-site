#!/usr/bin/env python3
"""Fecha a linha do tempo e a árvore até a Duda (Maria Eduarda), filha de Nilson. Idempotente; aplica sobre src/dados-orig/.
Só entram fatos ditos pelo Nilson (filha dele; acervo feito para ela). Sem data de nascimento."""
import json, pathlib
O = pathlib.Path('/home/claude/historia-e-sabores-avila-site/src/dados-orig')
L = lambda n: json.load(open(O/(n+'.json')))
S = lambda n, o: json.dump(o, open(O/(n+'.json'), 'w'), ensure_ascii=False, indent=1)
P = L('pessoas'); R = L('relacoes'); T = L('linha_do_tempo')
pid = {p['id']: p for p in P}
n = pid['nilson-jacob-da-costa']
duda = {k: None for k in n}
duda.update(id='maria-eduarda-duda', nome='Maria Eduarda (Duda)', ramo='minas', evidencia='P', aconfirmar=False,
            pais=['nilson-jacob-da-costa'], conjuge=None, filhos=[], foto=None, linha='costa', apelidos=['Duda'],
            conjuges=[], receitas=[], fontes=[], encontrado_por_este_estudo=False, possivelmente_vivo=False, divergencias=[],
            resumo='Filha de Nilson Jacob da Costa. Este acervo foi feito para ela: guardar o que é da família e perguntar o que ainda não se sabe.',
            evidencia_detalhe='Informação do próprio Nilson.')
if duda['id'] not in pid:
    P.append(duda)
if duda['id'] not in n['filhos']:
    n['filhos'].append(duda['id'])
if not any(a['tipo'] == 'genitor_de' and a['para'] == duda['id'] for a in R['arestas']):
    R['arestas'].append({'tipo': 'genitor_de', 'de': 'nilson-jacob-da-costa', 'para': duda['id']})
CAM = ('Duda → Nilson Jacob da Costa → Ilmovir José da Costa → Zilda Jacob da Costa → Maria Cândida da Conceição (Tia Nica) → '
       'Joaquim Esteves de Avila (Joaquim do Morro Alto) → Major Manoel Francisco de Avila → Francisco Antonio de Avila → '
       'Capitão Antonio Joaquim de Avila → João de Avila da Silveira → Capitão João de Avila Raposo, na Ilha do Pico.')
ev = {'id': 'ev-duda-01', 'ano': 2026, 'data': '2026-11', 'titulo': 'Este acervo chega à Duda',
      'texto': 'Nilson Jacob da Costa reúne o livro, as fotos, as pesquisas e esta página num acervo privado para a filha, Duda. '
               'Pelo que o estudo apurou, o caminho de volta até o Pico é: ' + CAM +
               ' Do lado dos Costa, a linha passa por Manoel Amâncio da Costa (Sorriso) e Francisco Amâncio da Costa, de Araxá.',
      'lugar_id': 'brasilia', 'pessoas_ids': ['maria-eduarda-duda', 'nilson-jacob-da-costa', 'ilmovir-jose-da-costa', 'zilda-jacob-da-costa'],
      'nivel': 'P', 'fonte': [{'arquivo': 'pesquisa/arvore-genealogica-nilson.md'}],
      'nota': 'Informação do próprio Nilson; alguns elos da linha ainda estão a confirmar pela família (veja a seção Pessoas).'}
T[:] = [e for e in T if e['id'] != ev['id']] + [ev]
S('pessoas', P); S('relacoes', R); S('linha_do_tempo', T)
print('duda ok', len(T))
