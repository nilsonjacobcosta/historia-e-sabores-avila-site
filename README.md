# História e Sabores Ávila (página interativa)

Página única, ilustrada e interativa sobre os 300 anos da família Ávila (os antepassados), da Ilha do Pico, nos Açores, a Minas Gerais e Brasília. Repositório **privado**, para uso da família. O acervo e as pesquisas ficam em `historia-e-sabores-avila`.

## Link da página
https://claude.ai/artifact/SaeBzhzkPyUkLHuUoead32 (artefato privado: abre só para quem tem acesso à conta do Nilson ou recebe o compartilhamento dele).

## Conteúdo
- Rota com mapa clicável, linha do tempo, árvore de pessoas com busca, galeria com ampliação, livro de receitas e legenda dos níveis de evidência (A, B, C, D, P, controverso).
- Pessoas que podem estar vivas aparecem só com nome e papel. Fotos de grupos com elas ficam ocultas até o visitante pedir.
- Divergências em aberto estão marcadas "a confirmar pela família" (ver `dados/LEIAME-DADOS.md`).

## Estrutura
- `index.html`: página final (gerada). Abre sem servidor só se os arquivos `dados/` e `img/` forem servidos por HTTP.
- `src/template.html`, `src/build.py`: fonte da página. `python3 src/build.py` junta o template, `design/base.css`, o sprite de ornamentos e o mapa.
- `src/sanitize.py`: lê `src/dados-orig/` (dados completos) e grava `dados/` (dados da página, já com as regras de privacidade).
- `design/`: direção visual "Cal & Basalto", CSS, ornamentos SVG, mapa e especificação da árvore.
- `dados/`, `img/`: dados em JSON e 194 imagens em WebP (sem EXIF/GPS).

## Direitos das imagens
Imagens do livro (© Fabricio de Avila Ferreira), de postagens de @fabriciodeavila e @jornal.interacao e de vídeos do canal Antonio Joaquim, reproduzidas sem fins comerciais, só para uso privado. Não republicar. Retirar a pedido.
