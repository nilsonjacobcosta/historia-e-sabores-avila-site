"""Gera dados/receitas_detalhe.json a partir do acervo (estudos/receitas e pesquisa/receitas).

Idempotente. Lê só arquivos do acervo; não inventa nada. Cada receita recebe:
  resumo, corpo (ingredientes/modo de fazer na ordem do livro), etiqueta (texto da etiqueta do livro),
  notas_leitura, oque, origem, variacoes, familia, diverg, perguntas, outros, parecidas, fontes.
"""
import json, re, pathlib

SITE = pathlib.Path('/home/claude/historia-e-sabores-avila-site')
ACERVO = pathlib.Path('/home/claude/historia-e-sabores-avila')


def limpa_links(t):
    # [texto](caminho-relativo) -> texto ; mantém só links http(s)
    t = re.sub(r'\[([^\]]+)\]\((?!https?:)[^)]*\)', r'\1', t)
    return t


JARGAO = [
    (r'correção do relatório do juiz,? [A-Z]\d+', 'correção na revisão da pesquisa'),
    (r'no relatório do juiz \([A-Z]\d+\)', 'na revisão da pesquisa'),
    (r'relatório do juiz,? [A-Z]\d+', 'revisão da pesquisa'),
    (r'relatório do juiz', 'revisão da pesquisa'),
    (r'li o texto via WebFetch', 'lido por resumo automático da página'),
    (r'abertas? com WebFetch', 'abertas por resumo automático da página'),
    (r'WebFetch', 'resumo automático da página'),
    (r'resumido pela ferramenta', 'resumido automaticamente'),
    (r'leitura minha, não afirmação', 'interpretação da pesquisa, não afirmação'),
    (r'leitura minha', 'interpretação da pesquisa, não do livro'),
    (r'inferência minha', 'inferência da pesquisa'),
    (r'observação minha', 'observação da pesquisa'),
    (r'suposição minha', 'suposição da pesquisa'),
    (r'especulação minha', 'especulação da pesquisa'),
    (r'\*\*especulação\*\* minha', '**especulação** da pesquisa'),
    (r'por mim\b', 'pela pesquisa'),
    (r'na minha leitura', 'na leitura da pesquisa'),
    (r'em minhas leituras', 'nas leituras da pesquisa'),
    (r'(especulação|observação|interpretação|comparação|hipótese|inferência|suposição) (culinária )?minha', r'\1 \2da pesquisa'),
]


def limpa_jargao(t):
    for a, b in JARGAO:
        t = re.sub(a, b, t)
    return t


def blocos(texto):
    return [b.strip('\n') for b in re.split(r'\n\s*\n', texto) if b.strip()]


def parse_estudo(path):
    txt = path.read_text()
    corpo, etiqueta, notas = [], [], []
    for m in re.finditer(r'<!--\s*(?:d[uú]vida|sic|nota):\s*(.*?)\s*-->', txt, re.S):
        notas.append(m.group(1).strip())
    txt = re.sub(r'<!--.*?-->', '', txt, flags=re.S)
    sub = None
    visto_titulo = False
    for b in blocos(txt):
        s = b.strip()
        if s.startswith('# '):
            continue
        if s.startswith('*Receita ') and 'Página PDF' in s:
            continue
        if s.startswith('## '):
            if not visto_titulo:
                visto_titulo = True
                continue
            sub = s[3:].strip()
            corpo.append({'t': 'sub', 'texto': sub})
            continue
        if s.startswith('### '):
            corpo.append({'t': 'sub', 'texto': s[4:].strip()})
            continue
        if s.startswith('!['):
            continue
        if s.startswith('(') and 'img-' in s:
            continue
        linhas = s.split('\n')
        if all(l.lstrip().startswith(('- ', '* ')) for l in linhas):
            corpo.append({'t': 'ing', 'itens': [re.sub(r'^\s*[-*]\s+', '', l).strip() for l in linhas]})
            continue
        if s.startswith('>'):
            etiqueta.append(' '.join(re.sub(r'^>\s?', '', l).strip() for l in linhas).strip())
            continue
        if re.match(r'^\*\*[^*]+:\*\*\s*$', s):
            corpo.append({'t': 'sub', 'texto': s.strip('*: ').strip()})
            continue
        s = re.sub(r'^Etiqueta \(texto sobre a imagem\):\s*', '', s)
        linhas = s.split('\n')
        if re.match(r'^\*\*[^*]+:\*\*\s*\S', s):
            etiqueta.append(' '.join(l.strip() for l in linhas))
            continue
        if len(s) < 45 and s.endswith(':') and '\n' not in s:
            corpo.append({'t': 'sub', 'texto': s.rstrip(':').strip()})
            continue
        corpo.append({'t': 'p', 'texto': ' '.join(l.strip() for l in linhas)})
    etiqueta = [e for e in etiqueta if e]
    return corpo, etiqueta, notas


MAPA = [('o que a receita', 'oque'), ('o que é a receita', 'oque'), ('resumo da receita', 'oque'), ('cruzamento com o instagram', 'instagram_nota'), ('receitas parecidas', 'parecidas_txt'), ('origem', 'origem'), ('varia', 'variacoes'), ('coer', 'familia'),
        ('diverg', 'diverg'), ('pergunt', 'perguntas')]


def parse_readme(path):
    txt = path.read_text()
    secs, outros = {}, []
    atual = None
    buf = []

    def fecha():
        if atual is None:
            return
        corpo = '\n'.join(buf).strip()
        if not corpo:
            return
        chave = None
        for pref, k in MAPA:
            if atual.lower().startswith(pref):
                chave = k
        if chave:
            secs[chave] = limpa_links(corpo)
        else:
            outros.append({'titulo': atual, 'texto': limpa_links(corpo)})

    for l in txt.split('\n'):
        if l.startswith('## '):
            fecha()
            atual = l[3:].strip()
            buf = []
        elif atual is not None:
            buf.append(l)
    fecha()
    # receitas parecidas: linha final ou seção própria
    parecidas = []
    txt = txt.replace('## Receitas parecidas no livro\n', 'Receitas parecidas no livro: ')
    for l in txt.split('\n'):
        if l.strip().lower().startswith('receitas parecidas'):
            for a, b in re.findall(r'(\d+)\s+a\s+(\d+)', l):
                parecidas += list(range(int(a), int(b) + 1))
            l2 = re.sub(r'\d+\s+a\s+\d+', '', l)
            parecidas += [int(n) for n in re.findall(r'\b(\d{1,2})\b', l2.split(':', 1)[-1])]
    # tira a linha de 'receitas parecidas' do último bloco, se estiver colada
    for k in list(secs):
        secs[k] = '\n'.join(x for x in secs[k].split('\n') if not x.strip().lower().startswith('receitas parecidas')).strip()
    return secs, outros, sorted(set(parecidas))


def parse_fontes(path):
    """Devolve (fontes, extras). extras = linhas soltas do fontes.md ('Sem fonte: ...', tentativas sem sucesso)."""
    if not path.exists():
        return [], []
    out, extras, cur = [], [], None
    for l in path.read_text().split('\n'):
        m = re.match(r'^(\d+)\.\s+(.*)', l)
        if m:
            cur = {'n': int(m.group(1)), 'ref': m.group(2).strip(), 'url': None, 'nivel': None, 'nota': None, 'consulta': None}
            out.append(cur)
            continue
        if cur is None:
            continue
        if l.strip() and not l.startswith((' ', '\t', '#', '-')):
            extras.append(limpa_links(l.strip()))
            continue
        u = re.match(r'^\s*-\s*URL:\s*(\S+)', l)
        if u:
            cur['url'] = u.group(1)
        c = re.match(r'^\s*-\s*Consulta:?\s*(.*)', l)
        if c:
            cur['consulta'] = c.group(1).strip()
        n = re.match(r'^\s*-\s*N[ií]vel de evid[eê]ncia:\s*(.*)', l)
        if n:
            txt = n.group(1).strip()
            m2 = re.match(r'^(A|B|C|D|P|controverso)\b\s*(.*)', txt)
            if m2:
                cur['nivel'] = m2.group(1)
                rest = m2.group(2).strip()
                if rest.startswith('('):
                    i = rest.find(')')
                    rest = (rest[1:i] + rest[i + 1:]) if i > 0 else rest[1:]
                cur['nota'] = rest.strip() or None
            else:
                cur['nota'] = txt
    return out, extras


def resumo(oque):
    if not oque:
        return ''
    t = re.sub(r'\*+', '', limpa_links(oque)).replace('\n', ' ').strip()
    t = re.sub(r'\[\d+(?:, \d+)*, ?[A-DP]\]', '', t)
    partes = re.split(r'(?<=[.!?])\s+', t)
    r = ''
    for p in partes:
        if len(r) >= 90:
            break
        if r and len(r) + len(p) > 230:
            break
        r = (r + ' ' + p).strip()
    return r


def main():
    receitas = json.loads((SITE / 'dados/receitas.json').read_text())
    out = {}
    for r in receitas:
        est = ACERVO / r['estudo']
        pes = ACERVO / r['pesquisa']
        d = {'id': r['id']}
        if est.exists():
            corpo, etiqueta, notas = parse_estudo(est)
            d.update(corpo=corpo, etiqueta=etiqueta, notas_leitura=notas)
        else:
            d.update(corpo=[], etiqueta=[], notas_leitura=[])
        if pes.exists():
            secs, outros, parecidas = parse_readme(pes)
            d.update(secs)
            d['outros'] = outros
            d['parecidas'] = [n for n in parecidas if n != r['numero']]
            d['fontes'], d['fontes_extra'] = parse_fontes(pes.parent / 'fontes.md')
            d['resumo'] = resumo(secs.get('oque', ''))
        else:
            d['resumo'] = ''
        d['resumo'] = limpa_jargao(d.get('resumo', ''))
        for k in ('oque', 'origem', 'variacoes', 'familia', 'diverg', 'perguntas', 'instagram_nota'):
            if d.get(k):
                d[k] = limpa_jargao(d[k])
        d['notas_leitura'] = [limpa_jargao(x) for x in d.get('notas_leitura', [])]
        d['outros'] = [{'titulo': o['titulo'], 'texto': limpa_jargao(o['texto'])} for o in d.get('outros', [])]
        for f in d.get('fontes', []):
            for k in ('ref', 'nota', 'consulta'):
                if f.get(k):
                    f[k] = limpa_jargao(f[k])
        d['fontes_extra'] = [limpa_jargao(x) for x in d.get('fontes_extra', [])]
        out[r['id']] = d
    (SITE / 'dados/receitas_detalhe.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')))
    sem = [k for k, v in out.items() if not v.get('corpo')]
    sem_res = [k for k, v in out.items() if not v.get('resumo')]
    print('receitas', len(out), 'sem corpo', sem, 'sem resumo', sem_res)


if __name__ == '__main__':
    main()
