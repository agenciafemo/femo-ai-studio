# Preparar clientes a partir do Norteia

O Norteia pode fornecer a base cadastral e estratégica inicial. O Studio acrescenta pesquisa externa, evidências, propostas, produção e aprendizado. A integração desta versão é de leitura: navegador/conector autorizado ou exportação local. O helper não faz chamadas de rede e não grava no Norteia.

## Caminho simples

> Leia SKILL.md e docs/NORTEIA.md. Consulte os clientes da nossa organização no Norteia em modo de leitura. Prepare as bases privadas dos clientes vigentes, aproveitando os campos disponíveis. Não faça pesquisa profunda de todos. Mostre quais já têm contexto útil e quais dependem de informações da equipe. Preserve decisões aprovadas e não publique os cadastros no GitHub público.

A IA deve confirmar o ambiente e a organização antes de ler cadastros. Nome parecido de projeto, configuração antiga no código ou staging não comprovam produção. Usar apenas os dados necessários; não consultar cofre, contatos pessoais, portal com token, financeiro ou credenciais para preparar conteúdo.

## Dados que podem entrar

- Cadastro mínimo: ID estável, organização, nome, segmento, escopo de tráfego e encerramento, quando disponíveis.
- Perfil de conteúdo: resumo da marca, posicionamento, serviços, público, objeções, voz, vocabulário, CTAs e restrições.
- Em rodada específica: conhecimento, afirmações e regras com origem, estado e validade; referências e arquivos cuja leitura foi autorizada. A primeira preparação não precisa baixar tudo.

A cor de destaque da interface do app não é paleta oficial. Formalidade e limite de emoji podem ser defaults de formulário. Serviços listados não identificam automaticamente a oferta prioritária. Dados cadastrais não definem objetivo comercial, manual vigente, direitos de imagem ou aprovação técnica.

## Exportação mínima e preparação local

Formato: JSON com schema_version: 1, source: norteia, collected_at: data ISO, organization_id e clients: lista. Cada cliente contém id UUID, organization_id, name, segment, traffic_only, ended_at, updated_at e content_profile. O profile é opcional. Um exemplo completamente fictício está em examples/norteia-minimo.json.

~~~bash
python scripts/norteia.py projetos/carteira-norteia/exportacao-minima.json --organizacao ID_DA_ORGANIZACAO --base projetos/clientes
~~~

O comando cria um dossiê por cliente, fontes locais e CARTEIRA-NORTEIA.md com links. O vínculo usa ID externo e registro local, preservando a pasta quando o nome muda. Cadastros encerrados até a data da coleta são pulados; --incluir-encerrados permite incluí-los quando isso fizer parte da missão. O comando não pesquisa perfis do Instagram e não conecta contas.

A identificação cadastral é registrada como tal. Os demais campos recebidos entram como hipóteses para revisão; não são promovidos a marca aprovada. Campos vazios continuam vazios. O relatório de lacunas indica o que falta para planejamento e design. O objetivo comercial deve ser definido com a equipe.

Execute uma preparação da carteira por vez. Repetir a mesma exportação não duplica o cliente nem seu histórico. Uma fonte nova que diverge do valor local gera proposta e conflito; não substitui conteúdo aprovado. Compare as fontes e registre a decisão. Registros fora da exportação não são apagados nem encerrados automaticamente. Não interpretar uma coleta parcial como carteira completa.

## Carteira real e repositório público

Os dados reais ficam em projetos/, ignorado pelo Git. O pacote público distribui método, código e exemplo fictício, sem nomes, IDs, notas ou materiais dos clientes. Em outro projeto, use uma pasta privada e confira se nenhum arquivo já está rastreado pelo Git; .gitignore não remove arquivos que já foram versionados.

Uma base existente do cliente continua sendo referência. Vincule-a no novo dossiê e leia seu status e decisões antes de pesquisar ou criar. Não começar a identidade do zero nem copiar o manual de outro cliente. Tráfego contratado não autoriza uma missão de conteúdo orgânico por dedução.

## Briefings e afirmações: validade antes de reutilizar

Quando uma missão exigir client_knowledge_items, considerar apenas itens ativos e dentro de effective_from/effective_until. Preservar os demais como histórico, fora da orientação operacional atual. Em client_content_claims, separar approved, prohibited e review_required; aprovação administrativa não é comprovação científica. Verificar validade e fonte. Regras gerais por segmento só se aplicam ao cliente e canal correspondentes.

Não somar “campos preenchidos” como prova de prontidão criativa. Uma ficha pode ter muitos textos e ainda faltar a pergunta central: qual objetivo e qual decisão precisamos influenciar agora?
