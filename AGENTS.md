# FEMO AI Studio

Leia `SKILL.md` para pesquisa, conteúdo, vídeo ou design e somente as referências relevantes. Use português brasileiro. Este repositório é um pacote de distribuição; materiais de clientes pertencem a `projetos/`, que é ignorado pelo Git.

Preserve brutos, referências recebidas e versões aprovadas. Não inclua arquivos de clientes, chaves, transcrições privadas ou fontes licenciadas em commits. Não instale dependências nem use serviços pagos se o pedido não autorizar essa etapa.

Validação do pacote: `python -m unittest discover -s tests -v`. O teste de renderização necessita FFmpeg e FFprobe; ele informa skip se faltarem. Verificação manual do PDF: `python scripts/audit_pdf.py docs/GUIA-FEMO-AI-STUDIO.pdf`, depois renderizar e examinar as páginas.

Arquivos públicos de descoberta são adaptadores; o conteúdo canônico da skill está na raiz. Para distribuição em outra pasta, use `scripts/install_skill.py`.

Para clientes: docs/CLIENTES.md e references/pesquisa-e-dossie.md. O catálogo em docs/CATALOGO.md é o ponto central de funções. Não leia todas as skills a cada tarefa. Conservar as licenças dos terceiros e adaptar caminhos globais à base do cliente. Antes de commit público, conferir que projetos/, dados privados e credenciais continuam fora dos arquivos rastreados. O verificador estrutural não aprova a pesquisa nem as peças.
