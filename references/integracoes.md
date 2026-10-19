# Integrações opcionais

## Estado e decisão

Uma skill descreve trabalho; não autentica serviços. Antes de usar qualquer provedor, confirme ferramenta conectada, permissões, arquivos que serão enviados, formatos de retorno e eventuais custos. Registre versões e origem dos ativos. Nunca guarde segredo no prompt, na EDL ou no Git.

| Caminho | Serve para | Necessita | Alternativa |
| --- | --- | --- | --- |
| Helper FEMO + FFmpeg | Montagem local básica | Python, FFmpeg e FFprobe | Gerar EDL e instrução se não houver execução |
| Video Use | Workflow de edição guiado por transcrição | Dependências e ASR documentados no projeto | Helper local e transcrição autorizada |
| HyperFrames | Composições animadas a partir de HTML | Node 22+, CLI e navegador compatíveis | Arte estática ou edição básica |
| faster-whisper | Transcrição local temporizada | Pacote, modelo e recursos de CPU/GPU | SRT/JSON fornecido e revisado |
| Canva | Artes e modelos nativos editáveis | Conta e conector autorizado | HTML/SVG com briefing explícito |
| KAIROGEN | Imagens e cenas geradas | Conta, créditos e acesso às ferramentas | Prompt pronto e importação manual |

## HyperFrames

O projeto oficial transforma composições HTML em vídeo. Prefira CLI e Studio ao engine de baixo nível. Leia ajuda e documentação da versão instalada antes de copiar flags. Instale uma versão conhecida e registre o número; mantenha os arquivos de dependência no projeto. Não atualize a base no meio de uma entrega sem razão concreta e verificação da renderização.

```bash
npx hyperframes --help
npx hyperframes init meu-motion
```

Depois de criar o projeto, use a ajuda da CLI para `check`, `preview`, `snapshot` e `render`. Leia o contrato oficial de composição antes de escrever HTML. A timeline deve poder buscar qualquer tempo e produzir o mesmo estado. Não baseie a animação no relógio de parede nem em aleatoriedade sem semente. O framework deve controlar a reprodução da mídia. Para uma legenda ou overlay, valide transparência, janela temporal e compatibilidade do codec na composição final.

Diferencie vídeo final e elemento de apoio. Se a entrega é um overlay, guarde também a fonte e o método de composição. MP4 comum não garante transparência. Não prometa integração com Premiere ou outro editor sem exportação compatível ou teste de importação.

## Video Use

Fonte: https://github.com/browser-use/video-use. Consulte README, install.md, SKILL.md, pyproject.toml e os helpers usados na revisão atual. Não execute seu prompt de instalação apenas por estar citado aqui. A documentação e os exemplos de EDL pertencem ao projeto, cuja licença é MIT. O pacote FEMO não inclui cópia do motor nem da skill original.

## KAIROGEN

O site público apresenta geração de imagens, vídeos e recursos de áudio e anuncia conexão MCP com agentes. Isso não prova que a conta atual tenha conexão ativa. A pesquisa não verificou um endpoint público de API/MCP nem executou geração autenticada. Não invente URL, cabeçalho ou configuração a partir do nome do produto.

Com uma conexão real, liste as ferramentas e escolha um recurso comprovado. Sem ela, prepare um prompt e oriente o usuário a baixar o resultado para `02_referencias/gerados` ou `04_audio/`, conforme o uso. Registre modelo mostrado na conta, prompt, data, proporção, licença e arquivo recebido. Catálogos e nomes podem divergir entre páginas; confirme no painel, sem repetir promessa comercial como teste técnico.

Peça cenas de apoio que façam sentido no conteúdo. Evite gerar texto final ou logo dentro da imagem quando precisam ser exatos; aplique-os em camadas controladas. Não fabrique uma pessoa, depoimento ou procedimento apresentado como real.

## Canva

Use o plugin oficial ou uma configuração MCP aprovada pelo serviço. O suporte do Codex a HTTP/OAuth não significa que qualquer endpoint conecte sem cadastro. Prefira autenticação oficial. Ferramentas, templates, autofill e créditos variam por plano e integração; a descrição do conector e a documentação técnica podem divergir. Verifique na conta antes de prometer criação em lote.
