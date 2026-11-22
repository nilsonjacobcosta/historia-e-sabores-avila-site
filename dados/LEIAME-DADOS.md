# Dados da página "História e Sabores Ávila"

Gerado em 22/11/2026 a partir do repositório `historia-e-sabores-avila` (somente leitura). Uso privado da família. "Ávila" designa os antepassados.

## Arquivos
- `pessoas.json` (123 registros), `lugares.json` (25), `linha_do_tempo.json` (49 eventos, 1665 a 2025), `receitas.json` (76), `relacoes.json` (arestas e 194 fotos), `imagens.json` (de outro agente; não alterado).
- Campos de pessoa seguem o contrato do designer (`id, nome, nascimento, morte, lugar, ramo, evidencia, aconfirmar, pais, conjuge, filhos, foto, resumo`). Campos extras: `linha` (Pico, Antonio Joaquim, Três Cruzes, Morro Alto, Jacob/Naves), `conjuges`, `fontes` (caminho no repo e página PDF), `evidencia_detalhe`, `divergencias`, `nota_confirmar`, `encontrado_por_este_estudo`, `possivelmente_vivo`.
- `ramo`: `acores` (Pico/Faial), `minas` (todos os demais), `goias` (só Delica, que se mudou para Goiás). `lugar` usa os ids de `lugares.json`; os seis ids combinados com o designer existem (`pico, borda-do-campo, morro-alto, araxa, goias, brasilia`).
- Datas como no livro: ISO completo quando o dia consta; só o ano quando só ele consta.

## Critérios
- **Níveis**: P = narrativa do autor ou documento transcrito no livro (testamento, assento, carta, bíblia de Tibúrcio). Os documentos transcritos ficam em P, não em B, porque os originais não foram conferidos e as cotas são **[referência não verificada]**. D = legendas de Instagram e do vídeo de lançamento. B só para contexto histórico conferido por juiz (erupções de 1718/1720, Araxá em Goiás até 1816). `controverso` quando as fontes divergem.
- **Pessoas possivelmente vivas**: entra a pessoa sem data, lugar, cônjuge ou foto, só nome, papel, receitas e ascendentes falecidos. Regra: sem morte declarada no livro e nascida depois de cerca de 1910, ou de idade desconhecida e ativa em 2009 (ano do livro). Estão nessa condição, por exemplo, Dinorá (única dos doze irmãos viva quando o livro foi escrito), os filhos de Carico e Irinéa sem morte declarada, os filhos de Fiíca, Vó Cecília, Vó Maria, Titonho, Juvenal, a família Leopoldino, os netos autores de receitas e o autor. Fotos que contenham essas pessoas têm `contem_possivelmente_vivos: true` em `relacoes.json` (sugestão: consultar a família antes de exibir). Foram deixados fora a filha do aviador e os parentes sem papel no livro além de nomes em fotos (Dôra, Tereza Cristina, Maria Célia e Malvina aparecem só como "outras pessoas" da foto).
- **Escopo**: ficam de fora o ramo Paiva de Carrancas, a linha Ferreira de Aguiar/Paiva da coluna do Jornal Interação (João Ferreira de Aguiar, Cândida Umbelina, Bartolomeu, Emirena e Fernando Portella como a coluna os apresenta) e os homônimos do Arquivo Público Mineiro, sem parentesco demonstrado. Por decisão do Nilson (22/11), **Carlos (Carico) e Irinéa de Aguiar Avila ficam** na linha Avila; a ascendência de Irinéa não é detalhada. Também entram, por serem impressos no livro como ascendência direta, Nicolao Alves Portella de Oliveira, Maria do Carmo de Oliveira e Anna Candida de Oliveira (ver D15). Se for decidido que isso fere a exclusão, remover esses três nós.
- Coordenadas: só Araxá (ponto da antiga estação, citado em pt.wikipedia, nível D, precisão ~1 km). Os demais lugares têm `lat/lon` null; buscas por município não devolveram coordenadas legíveis.
- Citações curtas (máx. 25 palavras); receitas resumidas pelos nomes dos ingredientes, sem quantidades nem modo de preparo.
- Pessoas encontradas por este estudo (nível D, legenda de 30/05/2021): Ana Tereza da Rocha, Elias Pereira Guimarães, Maestro Elias Porfirio de Azevedo, Camilo Afonso de Almeida (`encontrado_por_este_estudo: true`). Nomes citados na mesma foto sem parentesco declarado (Marta, Marica, Chiquinha, Pe. Marcigaglia, Galdino criança) não foram registrados; comentaristas não entram.

## Lacunas
1. **O ramo que liga o Nilson ao livro não está no repositório.** Nenhuma aresta ou marca aponta para ele; a árvore cobre os dois troncos do autor (Morro Alto e Três Cruzes), o tronco comum (Pico, Antonio Joaquim) e a família de Adélia Benevides Jacob. Aguardar indicação do Nilson.
2. Datas de nascimento e morte ausentes para a maioria (o livro raramente as traz); nada foi estimado, exceto o ano 1965 do aviador (inferido de "39 anos") e idades do inventário de 1940.
3. Originais de testamentos, inventários e assentos não vistos; cotas **[referência não verificada]**.
4. Batismo de 1709, brasão de 1665 e a sesmaria "Pederneiras" (1802) não foram localizados fora do livro.
5. Fotos: `foto` de pessoa aponta para uma só imagem de `imagens.json`; nem todos têm retrato.

## Divergências conhecidas (todas "em aberto, a confirmar pela família")
- **D01** Foto da família de Zico e Adélia: 1927 (livro e vídeo) x 1928 (comentário do autor no Instagram).
- **D02** "Lorico" (livro) x "Lourico" (postagens) para Lourival.
- **D03** "Antonio Luiz Leite" (livro) x "Antonio Luiz da Silva Leite" (postagem de 2024).
- **D04** Maria Célia e Malvina: só numa legenda de foto (Cap. IV), sem filiação.
- **D05** Qual Francisco Antônio: o filho de Antonio Joaquim (pentavô materno), Chico do Muro (filho do Major) e, no APM, um "Francisco Antonio de Avilla" de 1819 sem parentesco demonstrado. O vídeo (4:52) não distingue.
- **D06** "Rua das Flores" (legenda do vídeo) x "Rua Capitão José Porfírio" (livro, mesmo desenho): provável, não confirmado, que sejam a mesma casa.
- **D07** Lico: "Manoel Antonio" (galeria, inventário) x "Manoel Joaquim" (etiquetas de receita).
- **D08/D09** Emigração de 1748 x erupções do Pico de 1718/1720; o número 461 não tem fonte.
- **D10** Sesmaria "Pederneiras" sem fonte independente.
- **D11** Dedicatória "14/8/94" na foto do aviador, incompatível com a vida dele (faleceu aos 39 anos); leitura incerta já no livro.
- **D12** Legenda do vídeo "Filhos de Adélia e Zico (1987)" inclui Orlando, genro.
- **D13** Marido de Iracema: o texto diz o primo "Zico", filho do "tio-avô José Antonio"; a etiqueta de receita diz José Antonio Ferreira Junior.
- **D14** Três "Ana Cândida" e várias "Candinha": Candinha (filha de Tibúrcio), Donana (filha de Joaquim Esteves) e Anna Candida de Oliveira; a "Vovó Candinha" (Cândida Umbelina) é de ramo arquivado.
- **D15** Portella: Ana Rosa de Jesus (mulher de Francisco Antonio) é filha de um Nicolao Alves Portella; Maria do Carmo (filha dele) casou com o tio materno Nicolao Alves Portella de Oliveira; o livro grafa também "Portela". Isso une as linhas Morro Alto e Três Cruzes e entra em tensão com a informação de que os Portella não chegam ao Nilson.
- **D16** Vila de Araxá em 1831 (postagem de 2023) x posse da primeira Câmara em 7/1/1833 (livro); a postagem escreve "Mariano".
- **D17** Casamento de Carico e Irinéa: 31/07/1910 (narrativa) x 30/07/1910 (cartão das bodas de ouro).
- **D18** Marianno aparece "solteiro, 36 anos" no inventário do pai, embora casado com Escolástica.
- **D19** Idem: cronologia dos casamentos de Marianno e dos filhos de Antonio Joaquim a conferir.
- **D20** Thereza Thomázia "Teixeira" x "de Jesus".
- **D21** Joaquim Esteves nascido em 1857 e morto em 1940 "com 82 anos".
- **D22** Nica: "Maria Cândida da Conceição" x "Maria Cândida de Avila"; marido Hilmovir/Ilmovir.
- Outras: "Borba do Campo" x "Borda do Campo"; grafias Fiíca/Fíica, Orlelimda, Thomázia; "Fazenda Boa Vista" aparece em dois contextos; quem é "o Capitão" (receita 29) e "o Major" (receita 39); dados de 1930 e 1919 da postagem de 2024 são relato oral (D/P).
- Mariquinha, Juvenal e Sá Jerônima: legendas das fotos possivelmente trocadas, a conferir no impresso.
