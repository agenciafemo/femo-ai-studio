# Validação da distribuição

Data: 19 de outubro de 2026. Plataforma local: Windows x64. Python 3.12.14, FFmpeg/FFprobe 9.0.2 e Node.js 24.16.0 disponíveis. Claude Code e Codex foram encontrados no computador. As versões citadas descrevem o teste local, não dependências mínimas universais.

## Executado

- Validador oficial quick_validate.py do Skill Creator: skill válida.
- Suíte inicial: 12 testes aprovados, incluindo geração e decodificação de mídia sintética.
- Após ajuste da normalização por quadros: um teste de regressão adicional aprovado, com intervalos fracionados, áudio ausente e offsets de legenda na timeline normalizada.
- Inventário com e sem áudio, geometrias diferentes, nomes com espaço/apóstrofo e hash dos brutos.
- Rejeição de caminhos fora do projeto, intervalos inválidos, números não finitos, dimensões ímpares, HDR e corte dentro de palavra.
- Exportação de prévia e versão final, com arquivo original preservado e nomes de entrega diferentes.
- Remapeamento de palavras e renderização com legenda gravada.
- Instalação portátil, repetição idempotente e preservação de uma skill preexistente diferente.
- PDF de 16 páginas renderizado e inspecionado visualmente; 39 links com destinos definidos e áreas de clique dentro das páginas.
- Skill instalada nos escopos de usuário do Claude Code e do Codex. Conteúdo canônico e cópias conferidos.

O GitHub Actions repete os testes do código atual e audita o PDF em Ubuntu. Consulte a execução vinculada ao commit publicado para confirmar seu resultado.

## Limites da verificação

A mídia de teste é sintética. Nenhum vídeo de cliente ou paciente foi necessário. A validação técnica não certifica decisões editoriais, alinhamento de uma transcrição real ou conformidade de uma peça específica.

Não foram executados: ASR com download de pesos, geração paga, chamadas autenticadas Canva/KAIROGEN, criação de composições HyperFrames nesta distribuição ou teste completo de todas as versões/modelos de Claude e Codex. Esses caminhos são documentados como opcionais e dependentes do ambiente. Nenhuma conta externa foi conectada pelo instalador.

## Reproduzir

```bash
python -m unittest discover -s tests -v
python scripts/audit_pdf.py docs/GUIA-FEMO-AI-STUDIO.pdf
```

FFmpeg e FFprobe são necessários para os testes de mídia. O teste informa skip quando ausentes. A auditoria do PDF requer pypdf. Construção do guia usa requirements-pdf.txt; nenhuma dessas bibliotecas é necessária para o helper básico de edição.

## Pesquisa e base replicável · 22/10/2026

- python -X utf8 -m unittest discover -s tests -v: 30 testes encontrados, 23 executados com sucesso e sete de mídia pulados por FFmpeg/FFprobe ausentes do PATH da sessão. Os testes novos cobrem lacunas impeditivas e complementares, fontes bloqueadas/inexistentes, hipótese versus confirmação, conflito, prazo de revisão, histórico, importação idempotente, preservação de cliente existente, dados inválidos e instalação portátil.
- Helper de benchmark: comparação com mediana conhecida, fontes rastreáveis, separação por métrica e collab, tratamento diferente de zero e contagem oculta, amostra insuficiente e valor numérico inválido.
- quick_validate.py do skill-creator: skill central e direção de carrosséis válidas. Dependência YAML já presente no computador; nenhuma instalação global efetuada nesta atualização.
- Onze arquivos Markdown próprios com links locais verificados, sem destino ausente. O pacote de distribuição preserva 84 arquivos originais dos dois fornecedores, conferidos byte a byte com os clones públicos. São treze + nove skills auxiliares; o SKILL raiz do segundo pacote é um roteador adicional.
- Materiais de clientes não foram copiados para o pacote público. projetos/ permanece ignorado; a pasta criada para um cliente também contém .gitignore. Os exemplos/testes usam identidades fictícias.
- Nenhuma nova pesquisa em perfil real foi executada nesta consolidação. Validação estrutural não demonstra qualidade de uma pesquisa futura, desempenho de conteúdo ou acesso ao Instagram. As ferramentas de navegação/conectores continuam sendo necessárias na sessão de uso.

## Versão 1.2.0 · 22/10/2026

- Suíte completa: 44 testes executados com sucesso no ambiente com FFmpeg/FFprobe disponíveis. Inclui renderizações sintéticas e instalação portátil, além dos novos cenários Norteia e qualidade. A ausência de FFmpeg descrita acima pertence à sessão anterior de validação.
- Importação Norteia: escopo de organização, lista de campos permitidos, exclusão de contatos/tokens, preservação de decisão local, conflitos em atualização divergente, repetição sem duplicatas, vínculo por ID e encerramento. Objetivo e marca não são aprovados automaticamente.
- Um bloqueio temporário de rename no Windows foi observado durante a cópia de instalação; foi adicionado retry limitado, sem sobrescrever destino existente, e teste específico. A suíte completa passou depois do reparo.
- QA: contraste preto/branco, simetria, pares de baixo contraste, cores/metas inválidas, normalização de espaços/Unicode e detecção de alteração em negação e número.
- Preparação real da carteira executada em projetos/ com dados restritos. Segunda execução não criou nem atualizou dossiês. Nenhuma pesquisa aprofundada de Instagram foi simulada ou afirmada como concluída. O registro privado contém os detalhes, fora do Git.
- Fontes, licenças dos terceiros e vínculo com bases anteriores foram preservados. O repositório público contém apenas método, helpers e exemplo fictício.

## Versão 1.3.0 · contexto por entrega

- Suíte completa: 50 testes executados com sucesso, incluindo renderização e instalação portátil.
- Novos cenários: copy e key visual com dependências distintas; seleção apenas das evidências relevantes; preparação versionada sem alterar o dossiê; conflito preservado; entrada desconhecida rejeitada; campos do catálogo compatíveis com a base.
- O comando entregas.py tipos apresentou os dez contratos. A skill central passou no quick_validate.py e os links dos sete documentos de entrada revisados foram conferidos.
- CONTEXTO.json e BRIEFING.md são preparação de trabalho; nenhum resultado de arte, gravação, publicação ou validação técnica foi simulado. Não foram criadas entregas extras para os clientes reais nesta ampliação.
