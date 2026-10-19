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
