# Edição de vídeo

## Escolha editorial antes do filtro

Defina uma ideia central, público, destino, duração pretendida e material aproveitável. Em fala, procure tomada completa, intenção, pausas expressivas e continuidade. Corte tentativas repetidas e hesitações somente quando melhorarem a compreensão. Não remova negações, condições ou ressalvas para criar uma afirmação mais forte. Um vídeo sem fala pede seleção visual e ritmo próprios.

Analise primeiro o som e as transcrições temporizadas. Confira frames na abertura, em mudanças de enquadramento, nos cortes candidatos e nas cenas de apoio. Isso evita examinar milhares de imagens sem função editorial. Para cenas que dependem de ação visual, veja mais amostras e não tire conclusões só da transcrição.

## Ferramentas e escopo

O helper FEMO é uma base local independente: usa FFmpeg para uma lista de cortes, padroniza geometria e taxa de quadros, acrescenta áudio silencioso quando ausente e exporta H.264/AAC. Não escolhe tomadas por conta própria e não faz ASR, trilha, motion ou color grading avançado.

Video Use é uma alternativa opcional para um pipeline orientado por transcrição. Sua documentação descreve helpers, EDL e ferramentas de inspeção temporal. Leia a instalação e os schemas da versão escolhida; não use a EDL FEMO nos scripts externos sem adaptar o contrato. O provedor de ASR descrito pelo projeto é externo e demanda conta/credencial. Não faça upload de brutos sem autorização para esse destino.

Para ASR local, pode-se instalar faster-whisper em ambiente isolado. Ele suporta timestamps por palavra. A primeira carga de um modelo pode baixar arquivos. Confirme esse download antes de fazê-lo; CPU é uma alternativa quando CUDA não existe. Mantenha JSON temporal e SRT, e revise nomes próprios e linguagem técnica. O pacote não inclui pesos nem exige uma conta de ASR.

## Contrato da EDL FEMO

Salve em `05_projeto/edl.json`. Todos os caminhos de mídia são relativos à raiz `project_root`. A raiz é relativa ao arquivo da EDL, deve conter as pastas do projeto e não admite caminhos de origem fora de `01_brutos`. A montagem segue a ordem de `segments`.

```json
{
  "schema_version": 1,
  "project_root": "..",
  "output": {"width": 1080, "height": 1920, "fps": 30, "fit": "contain"},
  "segments": [
    {"source": "01_brutos/tomada01.mp4", "start": 2.0, "end": 8.5},
    {"source": "01_brutos/tomada02.mp4", "start": 1.2, "end": 7.0}
  ]
}
```

`contain` preserva todo o quadro e completa o espaço com verde FEMO. Para outra marca, configure `background` em hexadecimal, sem #. `cover` preenche recortando o centro: só use após conferir rostos, gestos e textos. Para enquadramento por plano ou animado, crie uma composição dedicada em vez de fingir que o recorte central resolve tudo.

Valores de largura e altura precisam ser pares. FPS deve ser de 1 a 60. Limites temporais devem caber na duração real do arquivo e ter pelo menos um quadro. Áudio é mantido em tempo normal. Não há ajuste automático de velocidade para forçar duração. O helper recusa PQ/HLG: trate HDR de forma explícita em um pipeline validado antes de montar.

```bash
python scripts/femo.py validate projetos/meu-video/05_projeto/edl.json
python scripts/femo.py render projetos/meu-video/05_projeto/edl.json --preview
python scripts/femo.py render projetos/meu-video/05_projeto/edl.json
```

A prévia usa até 540 pixels de largura. Intermediários normalizados em FFV1/PCM evitam uma segunda compressão com perdas antes da codificação final. Isso consome disco; não confunda com recuperar qualidade perdida na origem. O relatório compara duração, áudio e geometria, mas marca a revisão criativa como pendente.

## Legendagem

Guarde tempos na origem e recalcule para a saída. Para um trecho original de 20 a 25 segundos que começa aos 5 segundos da edição, uma palavra aos 21 segundos vai para 6 segundos da montagem.

O helper aceita um JSON temporal criado por ASR ou revisado manualmente:

```json
{"words": [
  {"source": "01_brutos/tomada01.mp4", "start": 2.2, "end": 2.7, "text": "Sua"},
  {"source": "01_brutos/tomada01.mp4", "start": 2.8, "end": 3.3, "text": "marca"}
]}
```

```bash
python scripts/femo.py captions CAMINHO/05_projeto/edl.json CAMINHO/05_projeto/palavras.json
```

O resultado é SRT na timeline final. Palavras atravessadas por um corte causam erro: ajuste o corte ou revise o alinhamento. Para gravar legendas na imagem, inclua `caption_srt: "05_projeto/legendas.srt"` na EDL; `caption_font` aceita o nome da fonte instalada. O filtro libass é obrigatório. Sem a fonte, libass pode substituir: confira logs e aparência antes de aprovar. Fontes da marca podem ser fornecidas em `03_marca/fontes`; o helper não as redistribui.

Use unidades de leitura, sem caixa alta compulsória. Duas linhas e 32 a 42 caracteres por linha são pontos de partida editoriais, não limites oficiais. Teste no celular e no player de destino. Evite áreas de botões, nome e legenda da plataforma.

## Áudio e cor

Ouça cortes com fone. Fades curtos podem reduzir cliques, mas não corrigem uma sílaba cortada. Preserve respiração natural e não aplique denoise agressivo. Normalize usando medição e uma meta adequada ao destino; -16 LUFS estéreo e true peak de até -1,5 dBTP são uma referência de trabalho, não uma exigência universal do Instagram. Para meta precisa, use análise e processamento em duas passagens e meça a saída.

Corrija exposição e balanço quando necessário; compare pele, branco e textura. Detecte a transferência HDR na entrada. Converter para 8 bits ou escrever BT.709 no metadado não faz tone mapping. Mantenha o original e registre qualquer transformação.

## Revisão e retomada

Revise abertura, encerramento, cada emenda, mudanças de escala, textos, recortes e momentos de sobreposição. Confira nomes, números e sentido contra a origem. Salve pedido, EDL, ferramentas, versões, arquivos usados, pendências e entrega no project.md. Em revisão, altere o trecho solicitado e preserve escolhas aprovadas.

## Helper de ASR opcional

Depois de preparar faster-whisper e um modelo local, execute `python scripts/transcribe_local.py CAMINHO_DO_PROJETO 01_brutos/tomada01.mp4 --model CAMINHO_DO_MODELO`. O padrão impede download de pesos. `--allow-model-download` habilita esse download quando já autorizado. O helper gera JSON por palavra e SRT da origem, com revisão pendente. Use o JSON no comando captions para ajustar à montagem. O pacote não inclui modelos nem garante ausência de erro de reconhecimento.

## Duração e quadros

O helper normaliza cada segmento para um número inteiro de quadros na taxa de saída. Quando necessário, acrescenta menos de um quadro de sustentação de imagem e silêncio ao fim do segmento, sem ler fala além do intervalo solicitado. As legendas usam esses mesmos offsets normalizados, evitando que arredondamentos se acumulem ao longo dos cortes. A duração esperada no relatório é a duração normalizada, que pode ser ligeiramente maior que a soma dos intervalos de origem.
