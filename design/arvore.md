# Árvore genealógica interativa — especificação (SVG + JS puro)

## Dados
Entrada: `../dados/pessoas.json`. Campos usados por pessoa: `id`, `nome`, `nascimento`, `morte`, `lugar`, `ramo` (acores|minas|goias), `evidencia` (A|B|C|D|P|controverso), `aconfirmar` (bool), `pais` [ids], `cônjuge` id|null, `filhos` [ids], `foto` (opcional), `resumo`.
Construir a árvore **descendente** a partir de um ancestral raiz (ex.: o do Pico, 1709); cônjuge fica ao lado (nó duplo); árvores com mais de um pai/mãe são tratadas como DAG: o nó aparece sob o primeiro pai e ganha um "atalho" (ícone de ligação) sob o outro, sem duplicar a subárvore.

## Layout (calculado em JS, sem biblioteca)
- Orientação: **vertical** (gerações de cima para baixo) no desktop; **horizontal** (esquerda para direita, gerações em colunas) no mobile 400px para evitar largura infinita.
- Algoritmo tidy-tree simples: largura de folha = 1 unidade; pai centralizado sobre filhos; espaçamento 24px entre irmãos, 56px entre gerações. Recalcular no expand/collapse com transição de 250ms (desligada em reduced-motion).
- `<svg role="tree" aria-label="Árvore genealógica Ávila">` dentro de `.arvore` (rolável, `tabindex="0"` na área rolável). Pan por rolagem nativa; sem zoom por gesto obrigatório (botões +/- opcionais, 44px).
- Nó: `<g role="treeitem" aria-level aria-posinset aria-setsize aria-expanded (só se tem filhos) tabindex="-1" data-id>` com `<rect class="no">` (140x56, raio 6, borda na cor do ramo: azul/barro/verde) + `<text>` nome (t-p bold) + datas; pequeno selo de evidência (letra num circulo) no canto; ícone `#orn-confirmar` se `aconfirmar`. Filhos em `<g role="group">`. Conectores: `<path>` em L/curva suave, `aria-hidden`, cor --linha.

## Interações
- **Recolher/expandir**: clique/Enter no nó, ou Seta Direita (expande) / Seta Esquerda (recolhe). Botões "Expandir tudo" / "Recolher tudo" / "Abrir até geração N".
- **Foco em um ramo**: botão "Focar neste ramo" no painel do nó (ou tecla `F`): esmaece (opacity .25, `inert` visual via classe) tudo fora dos ancestrais e descendentes do nó e centraliza (`scrollIntoView({inline:'center',block:'center'})`, comportamento `auto` se reduced-motion). Filtro por ramo (chips açores/minas/goiás, `aria-pressed`) e "Limpar foco" (Esc).
- **Painel de pessoa** (abaixo no mobile, lateral no desktop; `aria-live="polite"`): nome, datas, lugar, resumo, selo de evidência, aviso "a confirmar pela família" se aplicável, links para histórias/fotos/receitas relacionadas e botão "Ir para o cartão".
- **Busca**: campo "Buscar pessoa" (combobox simples); ao escolher, expande ancestrais e foca o nó.
- Sincronia com o mapa: ao focar pessoa, dispara `window` evento `pessoa-selecionada` {id}; escuta `lugar-selecionado` (de mapa.svg) para destacar pessoas daquele lugar (contornó duplo).

## Teclado (padrão WAI-ARIA Tree View, roving tabindex)
Tab entra na árvore (nó atual ou raiz); Seta Baixo/Cima: próximo/anterior nó visível; Direita: expande, ou vai ao primeiro filho se já aberto; Esquerda: recolhe, ou vai ao pai; Home/End: primeiro/último visível; Enter/Espaco: seleciona (abre painel); `*`: expande irmãos; `F`: focar ramo; Esc: limpar foco; digitar letra: type-ahead por nome. Foco visível: contorno 3px --mar (--barro no tema escuro) fora do retangulo.

## Acessibilidade e fallback
- Alternativa textual obrigatória: a mesma estrutura em `<ul>/<li>` aninhados com `<details>`. Regra única: lista e árvore SVG nunca ficam expostas juntas a tecnologias assistivas; o botão "Ver como lista" (`aria-pressed`) alterna qual das duas está visível e exposta (a outra recebe `hidden`). Sem JS, só a lista é exibida.
- Nunca só cor: ramo tem também o rótulo textual e o padrão do filete (listrado/ pontilhado/ liso).
- Contraste AA nos nós; texto mínimo 14px; alvos 44px; `prefers-reduced-motion` sem animação; sem dependência externa (opcional: nada de d3).

## Estado e erros
Estado em memória (sem localStorage); `location.hash` `#pessoa=<id>` para compartilhar. Se um id de `pais/filhos` não existir, ignorar e registrar no console; pessoas sem ligação aparecem em "Sem lugar na árvore ainda" (lista abaixo) com aviso "a confirmar".

## Estilos
Reusar `base.css`: `.arvore`, `.no`, `.pessoa[data-ramo]`, `.selo-evidencia`, `.aviso-confirmar`. Adicionar `.no[aria-selected="true"]{stroke-width:3}`, `.esmãecido{opacity:.25}`.
