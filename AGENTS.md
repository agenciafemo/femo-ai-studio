# FEMO AI Studio

Leia `SKILL.md` para produção de vídeo ou design e somente as referências relevantes. Use português brasileiro. Este repositório é um pacote de distribuição; materiais de clientes pertencem a `projetos/`, que é ignorado pelo Git.

Preserve brutos, referências recebidas e versões aprovadas. Não inclua arquivos de clientes, chaves, transcrições privadas ou fontes licenciadas em commits. Não instale dependências nem use serviços pagos se o pedido não autorizar essa etapa.

Validação do pacote: `python -m unittest discover -s tests -v`. O teste de renderização necessita FFmpeg e FFprobe; ele informa skip se faltarem. Verificação manual do PDF: `python scripts/audit_pdf.py docs/GUIA-FEMO-AI-STUDIO.pdf`, depois renderizar e examinar as páginas.

Arquivos públicos de descoberta são adaptadores; o conteúdo canônico da skill está na raiz. Para distribuição em outra pasta, use `scripts/install_skill.py`.
