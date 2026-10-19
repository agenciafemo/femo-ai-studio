# Design com Claude e Codex

## Uma direção, diferentes ferramentas

O modelo de IA não define o formato editável. Escolha pelo destino: Canva quando pediram Canva; SVG para desenho vetorial simples; HTML/CSS para diagramação controlada e capturas; ferramenta de apresentações para PPTX. PDF e PNG são entregas de visualização, não equivalentes à fonte editável.

Leia o manual e veja referências reais. Separe fatos documentados, preferências do usuário e proposta criativa. Identifique paleta, papéis tipográficos, grid, margens, alinhamentos, tratamento fotográfico, densidade de texto e ritmo entre páginas. Conserve logo original e símbolos. Não redesenhe um logo por aproximação.

Para um cliente, use seus próprios arquivos. A identidade da FEMO na documentação deste pacote não se torna regra para todos os trabalhos da agência.

## Processo prático

1. Esclareça mensagem, objetivo, canal, proporção e formato editável. Reaproveite o briefing quando essas informações já existirem.
2. Extraia o sistema visual do manual, sem confundir imagens de inspiração com paleta oficial ou licença para copiar.
3. Crie uma peça piloto com conteúdo real. Verifique no tamanho final antes de expandir para uma série.
4. Gere variações de composição que preservem o sistema. Um carrossel precisa de sequência de raciocínio e variação de densidade.
5. Confira leitura, ortografia, quebras de linha, alinhamento, contraste, recortes, proporção do logo e fontes carregadas. Verifique no navegador `document.fonts.check` ou mecanismo equivalente quando disponível; declarar font-family não comprova uso.
6. Exporte e abra o arquivo final. Entregue também a fonte e os ativos necessários, respeitando licenças.

Para feed, 1080 × 1350 e para stories, 1080 × 1920 são formatos habituais do workflow, ajustáveis ao pedido. Para uma capa que também será recortada em perfil, confira a região de interesse nos formatos de exibição reais.

## HTML e SVG

Use dimensão explícita, fontes locais autorizadas ou fontes abertas com licença, imagens resolvidas e caminhos relativos. Um arquivo que só funciona com uma URL temporária não é uma fonte portátil. Inclua notas de exportação e não prometa editabilidade nativa em Canva ou PowerPoint por entregar SVG/HTML.

A base em `assets/templates/post-femo.html` serve como estrutura editável para a FEMO. Ela declara a tipografia pretendida e usa fallback identificado; não contém Hagrid Text. A IA deve verificar a fonte antes de apresentar a peça como aplicação final da marca.

Para o mockup, capture pelo navegador disponível. Se não houver motor de exportação, entregue o HTML/SVG e diga que o PNG/PDF não foi renderizado. Não invente screenshot.

## Canva

Com o conector autenticado, confira ferramentas e permissões disponíveis. Prefira um Brand Template aprovado para peças repetíveis. Leia os campos e use dados reais. Para uma nova direção, gere candidatos e apresente escolhas quando o fluxo exigir. Depois de editar, confirme o salvamento e entregue o link editável retornado pelo serviço.

Kit de Marca ajuda com ativos, cores e fontes, mas não garante por si só ritmo, enquadramento e hierarquia. Compare a primeira peça com a referência. Bloqueios de elementos podem preservar identidade e também impedir alterações; teste no modelo utilizado. Não publique ou compartilhe externamente uma arte apenas porque a edição foi solicitada.

Sem conexão, prepare o briefing e a fonte possível. Não diga que criou um design Canva nem substitua silenciosamente por uma imagem achatada.

## Claude e Codex

A direção e os critérios são os mesmos. Claude Code e Codex podem operar arquivos e ferramentas em ambientes habilitados. A disponibilidade de um gerador de imagens ou conector não é garantida pelo nome da IA. Use o que existe na sessão e registre o resultado real. A skill pública frontend-design da Anthropic é uma referência adicional de construção de interfaces; ela não é uma integração Canva nem um manual da FEMO.

## Anatomia do briefing e personagem

Use papel, contexto, referência, restrições e formato como campos de um briefing, convertendo adjetivos em critérios observáveis. A expressão premiado não substitui especificar grid, contraste e hierarquia. Consulte o exemplo em examples/carrossel-sobrancelhas.md no pacote de distribuição. Cinco passos em cinco slides precisam de uma estrutura que realmente comporte os cinco passos.

Confira que a foto e a referência citadas foram recebidas. Se faltarem, avance no texto e no mapa de layout e declare a dependência. Preserve a identidade da pessoa autorizada. Não invente anexos, depoimentos, resultados ou uma personagem apresentada como a pessoa real.
