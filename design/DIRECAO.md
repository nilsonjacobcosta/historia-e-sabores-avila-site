# Direção visual: "Cal & Basalto"

## Conceito
Uma parede de azulejo caiada que guarda um caderno de bordo. A página é **cal** (branco frio de parede acoreana), o texto é **basalto** (a pedra negra do Pico), o fio que conduz tudo é o **azul de azulejo** (mar e cerâmica), e o **barro** ocre e o **verde de cerrado** marcam Minas e Goiás. A família sai da ilha vulcanica e o azul "atravessa" a página como um traçado de mapa até chegar ao barro e ao verde. As receitas ficam em fichas de caderno com letra a mão (Caveat), o único toque manuscrito.
Regra de ouro: azulejo e ornamento ficam nas bordas, nós filetes e nós divisores; o texto sempre repousa em superficie lisa.
Evitado de proposito: creme+serif+terracota generico, roxo/azul-neon, Inter.

## Tokens (arquivo base.css) — AA verificado (razão de contraste sobre fundo)
| Token | Papel | Claro | Escuro |
|---|---|---|---|
| --cal | fundo | #F2F4F1 | #12171B (basalto) |
| --papel | superficies | #FFFFFF | #1B2228 |
| --tinta | texto (14,9:1 / 15,1:1) | #182026 | #E9ECE8 |
| --mar | azul de azulejo, links (8,6 / 9,1) | #1E3F94 | #9DB8F2 |
| --barro | ocre, receitas, alertas (5,6 / 8,3) | #9C4A1A | #E8A064 |
| --cerrado | verde, Goiás, "confirmado" (6,3 / 10) | #3F6322 | #A9CC7C |
Auxiliar: --tinta-2 (#4A545C / #A9B3BB, 7:1 e 8,5:1). Escuro automático por prefers-color-scheme; `[data-theme="light|dark"]` no `<html>` força o tema (botão de tema opcional). Cor nunca é o único sinal (selos têm letra, rótulo e borda).

## Tipografia (Google Fonts)
- Display: **Young Serif** (serifa humanista robusta, lembra letras de azulejo e placas). Títulos, anos, numeros dos passos.
- Texto: **Atkinson Hyperlegible** 400/700 (feita para legibilidade, boa para leitores mais velhos e telas pequenas).
- Mão: **Caveat** 400/700, só para notas, origem da receita e "a confirmar".
- Link sugerido: `family=Young+Serif&family=Atkinson+Hyperlegible:wght@400;700&family=Caveat:wght@400;700&display=swap`
- Escala fluida: corpo 16-17px; t1 1,15-1,3rem; t2 1,4-1,9rem; t3 1,8-2,8rem; t4 (herói) 2,4-4,6rem; etiqueta 14px. Linha 1,65 no corpo, 1,12 nos títulos; medida 65ch; `text-wrap: balance` em títulos, `pretty` em parágrafos.

## Grade e espaço
Mobile 400px: coluna única, gutter 16px, espaçamento base 4px (seções 64px). Tablet >=640: galeria 2-3 col, receita em 2 col. Desktop >=832 (52rem): container 72rem, herói 2 col, linha do tempo horizontal opcional, menu em linha. Alvos de toque >=44px.

## Motion
**Um momento orquestrado: a abertura.** (1) o Pico emerge da linha d'água (translateY+opacity, 700ms), (2) o traçado azul do mapa-miniatura corre da ilha até o ponto "Brasília" (7s no mapa completo, ao entrar na seção Rota), (3) o título sobe. O resto é discreto: `.revela` (fade+14px) por IntersectionObserver, moldura da foto inclina -0,6 grau no hover. `prefers-reduced-motion`: tudo estático, traçado já completo, sem scroll suave. Nada em loop.

## Mapa de seções (ordem e função)
1. **Cabeçalho** (sticky): marca-azulejo + nome, menu (hamburguer no mobile), alternador de tema.
2. **Herói**: título "História e Sabores: Ávila", subtítulo "300 anos, da Ilha do Pico a Brasília", Pico estilizado + ondas, selo 1709, CTA "Começar pela rota". Dedicatória curta a Duda.
3. **Rota (mapa)**: mapa.svg com pontos clicáveis; painel lateral/inferior mostra o lugar (texto, pessoas ligadas, fotos).
4. **Linha do tempo**: vertical no mobile, horizontal com snap no desktop; filtro por regiao; marcos com selo de evidência.
5. **Pessoas e árvore**: árvore interativa (ver árvore.md) + grade de cartões de pessoa.
6. **Histórias**: capitulos curtos em coluna de leitura (65ch), citacoes à mão, divisor de renda entre capitulos.
7. **Galeria**: fotos em molduras, lightbox acessivel (dialog), legendas e créditos.
8. **Livro de receitas**: cartões de receita (ingredientes marcáveis, modo de fazer numerado, nota da família); filtro por ramo.
9. **Fontes e evidência**: legenda dos níveis (A documento primário; B fonte secundária confiável; C tradição/livro sem documento; D indício fraco; P a pesquisar; Controverso: versões em conflito) + aviso "a confirmar pela família" + como contribuir.
10. **Rodapé**: selo, rosa-dos-ventos, nota de privacidade (família).

## Wireframe mobile (400px)
```
[ marca-azulejo  Ávila        ☰ ]  <- sticky 56px
-------------------------------
 ~~~ faixa de azulejo 56px ~~~
 ILHA DO PICO (silhueta+ondas)
 História e Sabores: Ávila     <- t4, balance
 300 anos, do Pico a Brasília
 [ Começar pela rota ]
 selo 1709
-------------------------------
 Rota  ~~ divisor ondas ~~
 [ mapa 400x260, pontos 44px ]
 [ painel do lugar (abaixo)  ]
-------------------------------
 Linha do tempo (vertical, no em losango)
 1709 ... [selo B]
 ... 
-------------------------------
 Pessoas: [árvore rolavel] / cartões 1 col
 Histórias: texto 65ch, 1 col
 Galeria: 2 col, lightbox tela cheia
 Receitas: ficha 1 col (ingredientes > modo)
 Fontes: legenda dos selos, aviso a confirmar
 Rodapé
```
## Wireframe desktop (>=1024)
```
[marca Ávila] Rota Tempo Pessoas Histórias Fotos Receitas Fontes [tema]
+---------------------------+--------------------+
| Título t4 + subtítulo CTA |  Pico + selo 1709  |   herói 2 col
+---------------------------+--------------------+
| mapa.svg (8/12)           | painel lugar (4/12)|   sticky ao lado
+---------------------------+--------------------+
| linha do tempo horizontal (snap) com filtro   |
+------------------------------------------------+
| árvore (largura total, foco por ramo)          |
| cartões de pessoa 3-4 col                      |
| histórias: coluna 65ch + margem com notas/fotos|
| galeria 4 col | receitas: ficha 2 col          |
```
## Acessibilidade (checklist)
AA em todos os pares; foco visível 3px; teclado em mapa, árvore, lightbox (dialog nativo, Esc fecha, foco volta ao gatilho); `alt` descritivo nas fotos (legenda como fallback); landmarks (header/nav/main/section com h2/footer) e link "pular para o conteúdo"; `lang="pt-BR"`; reduced-motion; nenhum conteúdo só por cor; ornamentos decorativos com aria-hidden.
## Restrições do artefato
Sem imagens remotas (fotos em data URI ou SVG inline), fontes só Google Fonts, scripts só cdnjs/jsdelivr versão fixa (a página deve funcionar sem nenhum), sem download/print/alert; lightbox com `<dialog>`, sem `alert`.
