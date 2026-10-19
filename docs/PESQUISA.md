# Pesquisa técnica e decisões FEMO

Revisão: 19 de outubro de 2026. A pesquisa distingue documentação consultada, decisões de implementação e testes realmente executados. Não houve geração paga nem teste de conta em Canva ou KAIROGEN.

## 1. Video Use: edição orientada por informação temporal

O projeto organiza edição com agentes a partir de transcrição e inspeções visuais dirigidas. Seu README descreve cortes, legendas, grafismos e revisão, com saída e memória por projeto. SKILL.md e install.md documentam um ambiente com Python, FFmpeg e um serviço de transcrição. Os helpers render.py e transcribe.py foram consultados para entender contratos e dependências.

**Decisão FEMO:** adotar leitura temporal e retomada de decisões, mantendo um helper básico independente, sem copiar o motor. Usar o projeto externo é opcional. Suas regras e esquemas não são automaticamente os do pacote FEMO. Melhorias desta distribuição estão na portabilidade, transparência de capacidade, organização e critérios de marca; não em um benchmark que prove um motor superior.

Fontes: [README](https://github.com/browser-use/video-use), [skill](https://github.com/browser-use/video-use/blob/main/SKILL.md), [instalação](https://github.com/browser-use/video-use/blob/main/install.md), [renderer](https://github.com/browser-use/video-use/blob/main/helpers/render.py), [transcrição](https://github.com/browser-use/video-use/blob/main/helpers/transcribe.py). Revisão de código registrada: `43cfc566833548093455c9d4a46bd69913b7e552`. Licença MIT.

## 2. HyperFrames: composição animada com fonte editável

O repositório e a documentação descrevem renderização de composições HTML, prévia e ferramentas de produção. Node.js 22+ consta no projeto consultado. O engine busca tempos para produzir quadros; por isso, a composição precisa reconstruir o estado na timeline. Fontes, mídia e runtime influenciam reprodutibilidade.

**Decisão FEMO:** usar como caminho de motion quando necessário, registrando a versão instalada e validando prévia e saída. Não exigir a instalação para um corte básico, não confundir MP4 com overlay transparente e não declarar suporte a um editor de terceiros sem testar a exportação. A documentação oficial deve ser lida na versão em uso.

Fontes: [repositório](https://github.com/heygen-com/hyperframes), [engine](https://hyperframes.heygen.com/packages/engine), [player](https://hyperframes.heygen.com/packages/player), [renderização](https://hyperframes.heygen.com/guides/rendering). Revisão registrada: `4c798f398dc36e2d2f7df9e48d3e1b9858e87628`. Licença Apache-2.0. O número de uma dependência consultada não foi usado como garantia de versão instalada.

## 3. FFmpeg: base local verificável

A documentação distingue corte, filtros, concatenação, reamostragem, legendagem e tratamento de cor. Padronização de formato, relógios de áudio/vídeo e compatibilidade de streams importam na montagem. Marcar um arquivo como SDR não converte sua transferência HDR.

**Decisão FEMO:** o helper usa lista de argumentos sem shell, verifica duração e entradas, mantém originais, normaliza segmentos em intermediários sem nova compressão com perdas e codifica a entrega em H.264/AAC. Ele rejeita HDR para tratamento deliberado, cria versões únicas e emite um relatório técnico. Fades curtos, metadados e exame de frames não substituem escuta e julgamento editorial.

Fontes: [filtros](https://ffmpeg.org/ffmpeg-filters.html), [ffprobe](https://ffmpeg.org/ffprobe.html), [formatos/concat](https://ffmpeg.org/ffmpeg-formats.html#concat), [download](https://ffmpeg.org/download.html). A licença do executável depende da build; o pacote não redistribui FFmpeg.

## 4. Transcrição: opção local e opção externa

Whisper é uma referência aberta de reconhecimento de fala. Faster-whisper oferece implementação baseada em CTranslate2 e saída com tempos por palavra. CPU, GPU, tipo de cálculo e modelo alteram recursos e desempenho. Download do modelo pode ocorrer na primeira carga.

**Decisão FEMO:** não tornar uma assinatura de ASR obrigatória nem baixar pesos sem necessidade. Aceitar texto temporal revisado, usar ASR local quando instalado e apropriado ou um provedor externo autorizado. Conferir erros de português, nomes técnicos e cortes nas fronteiras de palavras. O pacote não foi avaliado como sistema de transcrição clínica.

Fontes: [Whisper](https://github.com/openai/whisper), [faster-whisper](https://github.com/SYSTRAN/faster-whisper), [ElevenLabs Speech to Text](https://elevenlabs.io/docs/capabilities/speech-to-text). As licenças dos projetos abertos permanecem próprias.

## 5. Claude e Codex: instrução portátil e execução situada

As duas plataformas documentam skills como pastas com SKILL.md e recursos. Claude Code descobre skills de projeto em .claude/skills; a documentação Codex consultada usa .agents/skills. Escopo de sessão, nuvem, políticas e conectores não são equivalentes a acesso automático ao disco.

**Decisão FEMO:** um corpo canônico, adaptadores simples e instalador que copia os recursos completos. Pedidos em português, sem ferramentas com nomes inventados. O PDF funciona como guia; a execução depende de um ambiente habilitado. Teste do pacote com Python não é uma certificação de comportamento de todos os modelos das duas empresas.

Fontes: [Claude Code Skills](https://code.claude.com/docs/en/skills), [Claude Code setup](https://code.claude.com/docs/en/setup), [Codex Skills](https://developers.openai.com/codex/skills/), [Codex MCP](https://developers.openai.com/codex/mcp/). Os diretórios podem mudar: consulte a documentação ao atualizar o pacote.

## 6. Canva: modelo aprovado como base de repetição

A documentação do Canva diferencia geração, edição, ativos e modelos. Recomenda templates e preenchimento para resultados repetíveis, além de conferir contexto completo da marca. Acesso depende de autenticação, permissão e plano.

**Decisão FEMO:** usar o modelo nativo e o link editável quando o destino é Canva; verificar salvamento e aparência. Não alegar que HTML, PNG ou SVG equivalem a um design Canva. Planos de autofill/criação em lote apresentam diferenças entre páginas técnicas e descrição do conector; confirmar na conta, sem promessa universal.

Fontes: [MCP](https://www.canva.dev/docs/apps/mcp/), [boas práticas](https://www.canva.dev/docs/apps/mcp/best-practices/), [ferramentas e planos](https://www.canva.dev/docs/apps/mcp/tools/), [bloqueios de modelos](https://www.canva.com/help/brand-template-locks/).

## 7. KAIROGEN: fornecedor opcional, conexão não presumida

As páginas públicas apresentam geração de imagens, vídeos e áudio e anunciam MCP para agentes. Os catálogos exibidos variam entre páginas públicas; isso é informação comercial, não teste independente de cada modelo. A pesquisa não validou endpoint público, autenticação, chamadas ou retorno de uma conta.

**Decisão FEMO:** documentar o papel de geração e uma alternativa manual de importar o resultado. Exigir ferramenta conectada e permissão real antes de executar. Não inventar endpoint, não fixar preços e não afirmar que a plataforma edita um conjunto de brutos pelo simples fato de gerar clipes.

Fontes: [aplicativo público](https://app.kairogen.ai/), [apresentação e MCP anunciado](https://kairogen.ai/multimodelo). Recursos, limites, privacidade e créditos devem ser conferidos na conta antes de uso.

## 8. Anatomia do Prompt: transformar estilo em briefing verificável

O site foi lido no navegador em 19/10/2026. Organiza pedidos de carrossel por papel, contexto, referência, restrições e formato; demonstra escolha de referência, capa piloto e revisão dirigida.

**Adaptação FEMO:** trocar adjetivos vagos por decisões de layout, fonte, hierarquia, texto e imagem. Conferir anexos antes de citar uma pessoa. Separar geração fotográfica de texto final quando a precisão for importante. Uma referência inspira estrutura; não concede licença de cópia. O exemplo de sobrancelhas foi incluído a pedido do usuário, sem criar uma personagem inexistente.

Fonte: [Anatomia do Prompt](https://anatomiadoprompt.vercel.app/). O site orienta um processo criativo; não fornece evidência de resultado comercial garantido.

## 9. Identidade e referência didática

O manual FEMO enviado pelo usuário orientou paleta, tipografia declarada, logo e linguagem editorial. O guia de @igao.ia orientou somente a organização didática de passos e botões. As páginas e os ativos desses documentos não foram copiados para o guia; a cópia integral de ambos fica fora do repositório público. O logo FEMO é um ativo da marca, separado da licença de software.

## 10. Como verificar esta distribuição

Consulte docs/VALIDACAO.md para ambiente e testes efetivamente executados. Os testes locais usam mídia sintética, não pacientes ou vídeos privados. Revise também o PDF renderizado, as áreas clicáveis, os destinos dos botões, as cópias instaladas e o conteúdo do commit. Versões futuras precisam repetir as verificações que afetam o código alterado.
