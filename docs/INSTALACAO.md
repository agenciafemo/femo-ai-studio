# Instalação e primeiro uso

## Caminho recomendado

Baixe o ZIP do GitHub, extraia e abra a pasta extraída no Claude Code ou Codex. O repositório já contém AGENTS.md, CLAUDE.md e adaptadores nos diretórios de skills de projeto. Peça: Leia SKILL.md, verifique as ferramentas e prepare a pasta do meu trabalho. Não é necessário instalar uma skill global para usar esta pasta.

Se o chat aceita anexos, anexe o guia PDF. Caso contrário, informe seu caminho e peça a leitura. O repositório é a instrução executável; o PDF é o guia de entrada.

## O que precisa existir uma vez

- Claude Code ou Codex com sessão autenticada e acesso à pasta.
- Python 3.10+.
- FFmpeg e FFprobe no PATH, ou variáveis FFMPEG_BIN e FFPROBE_BIN.
- Espaço em disco para originais, intermediários e entrega.

A IA pode orientar a preparação. Baixe software das fontes oficiais. Não instale pacotes como se o PDF já concedesse acesso administrativo. Node.js 22+ é necessário quando o trabalho usa HyperFrames, não para o helper básico.

## Em outra pasta de trabalho

```bash
python scripts/install_skill.py --target C:/Trabalhos/MeuProjeto --agent both
```

No macOS ou Linux, use python3 se python não existir. O instalador copia a skill completa com os helpers e as referências. Ele não altera credenciais, instala dependências ou sobrescreve uma skill diferente. Se encontrar uma instalação diferente, informe outro destino ou faça a atualização consciente com backup.

Claude Code descobre `.claude/skills/femo-ai-studio/SKILL.md`. Codex descobre `.agents/skills/femo-ai-studio/SKILL.md`. A descoberta depende de versão, escopo e políticas do ambiente. Se não aparecer, abra a pasta correta, confira os arquivos e reinicie a sessão. Continua possível pedir explicitamente que a IA leia o SKILL.md.

## Chat, computador e nuvem

Chat comum pode trabalhar com anexos e ajudar no planejamento conforme as ferramentas disponíveis. Uma pasta no seu computador não fica acessível apenas por escrever o nome no chat. Use uma sessão com acesso local ou disponibilize os arquivos em um ambiente autorizado. Execução em nuvem tem dependências e armazenamento próprios; contas conectadas e pastas locais não se transferem automaticamente.

## Serviços opcionais

ASR local pode baixar modelos. ASR externo envia áudio ao provedor. Imagem, vídeo e áudio gerados podem consumir créditos. Autorize destino e material antes de enviar. Use variáveis de ambiente ou o fluxo oficial para credenciais. Não coloque chaves no chat ou em commit.

## Windows e instalação de usuário

Se o comando python não estiver disponível, o launcher `scripts/femo.ps1` procura um interpretador instalado ou o runtime já disponível no Codex. Exemplo: `./scripts/femo.ps1 doctor`. Ele não muda o PATH nem a política de execução do Windows. A IA também pode usar o caminho completo do interpretador.

Para registrar a skill nos diretórios de usuário, use `python scripts/install_skill.py --user --agent both`. Isso copia a skill para os escopos pessoais do Claude Code e do Codex, sem instalar programas ou substituir uma instalação diferente.
