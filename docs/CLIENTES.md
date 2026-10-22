# Um cliente novo, uma base própria

O FEMO AI Studio reúne pesquisa, estratégia, copy, design e vídeo em uma entrada: SKILL.md. Baixe o repositório completo e abra a pasta no Claude Code ou no Codex com acesso aos arquivos. Use o pedido abaixo; a IA executa os comandos. Você não precisa preencher o JSON manualmente.

> Leia SKILL.md. Cadastre o cliente [nome], perfil [URL]. Nosso objetivo é [resultado comercial ou “precisamos definir”]. Pesquise conteúdo próprio e referências, estude identidade e voz e monte o dossiê com evidências. Use os papéis de pesquisa disponíveis; diga se trabalhará em sequência ou com agentes. Não produza peças ainda. Ao terminar, mostre achados, contradições, o que já permite planejar e o que precisamos fornecer.

## Comandos locais

Python 3.10+, sem dependências extras. No Windows, use o interpretador disponível no computador se python não estiver no PATH. Caminhos são relativos à raiz do pacote nestes exemplos; dentro de uma instalação da skill, use o caminho completo do script e um destino do projeto de trabalho.

~~~bash
python scripts/clientes.py novo clinica-exemplo --nome "Clínica Exemplo" --instagram https://www.instagram.com/perfil-exemplo/
python scripts/clientes.py evidencia projetos/clientes/clinica-exemplo --arquivo pesquisa-coletada.json
python scripts/clientes.py campo projetos/clientes/clinica-exemplo objetivo --valor "Priorizar consultas de avaliação para o serviço X; medir solicitações qualificadas no período definido pela equipe" --estado confirmado --fontes BRIEF-001
python scripts/clientes.py verificar projetos/clientes/clinica-exemplo --etapa planejamento
python scripts/clientes.py relatorio projetos/clientes/clinica-exemplo
~~~

O arquivo de evidências é uma lista ou um objeto único no formato de templates/cliente/evidencia-exemplo.json. Registre a fonte BRIEF-001 antes de confirmar o objetivo. Comandos de registro não navegam nem pesquisam: a IA precisa usar um navegador/conector ou ler material fornecido e depois registrar o que realmente observou.

Campo aceita --arquivo para valor JSON complexo e --nota para tentativas, contexto ou motivo de não aplicabilidade. Estados: ausente, hipotese, confirmado, conflito, nao_aplicavel. “Não aplicável” exige justificativa; campos essenciais não podem ser dispensados assim. Atualizações guardam histórico e cópia anterior. Não altere dossie.json enquanto outro processo o atualiza.

## Pasta criada (privada por padrão)

~~~text
projetos/clientes/clinica-exemplo/
  AGENTS.md e CLAUDE.md   instruções portáteis de retomada
  dossie.json             fatos, hipóteses, evidências, estados e histórico
  DOSSIÊ.md               leitura organizada gerada do JSON
  LACUNAS.md              pendências, impacto e perguntas para a equipe
  entradas/              briefing e materiais originais
  pesquisa/              relatórios por papel, posts e amostragem
  identidade/            manual e aplicações aprovadas
  referencias/           fontes visuais e swipe contextualizado
  conteudo/              plano, copys e roteiros com versões
  producao/              fontes editáveis e ligações com projetos de vídeo
  entregas/              prévias e finais
  decisoes/              aprovações e aprendizados datados
  historico/             snapshots anteriores às atualizações
~~~

projetos/ é ignorado pelo Git público. Os dados de clientes existentes continuam onde estão; incorporar uma cliente existente significa apontar para sua base privada e mapear os campos, sem publicar sua pasta no Studio. Não mover nem apagar materiais para fazer uma migração automática. No destino externo, a pasta criada recebe seu próprio .gitignore; ele protege do commit acidental mas não substitui a escolha correta de repositório privado.

## O que precisa constar

O modelo em templates/cliente/campos.json define os itens, perguntas e etapas dependentes. Ele cobre identificação/perfil, objetivo e medida de sucesso, oferta prioritária, público e objeções, posicionamento, prova, voz, identidade vigente, regras de conteúdo, referências, amostra própria, benchmark, conversão, acervo, operação/aprovação e aprendizado.

Cada item contém valor, estado, fontes e data de revisão. O prazo de revisão é configurável por item; os valores iniciais são uma convenção operacional do pacote, não duração científica dos fatos. Reavalie antes da entrega se houve mudança mesmo dentro do prazo.

As etapas não exigem o mesmo grau de preenchimento: pesquisa pode começar com o perfil; planejamento exige objetivo, público, oferta, argumento, voz, contexto e limites; design final também exige identidade, ativos e formato/editor. Métricas indisponíveis não impedem inspiração visual, mas impedem comprovar desempenho. Pesquisa incompleta deve continuar visível como lacuna.

O comando verificar retorna 0 quando a etapa está estruturalmente pronta, 2 se há lacunas impeditivas e 1 se o arquivo é inválido. A pesquisa não recebe certificado de qualidade por ter campos preenchidos. O revisor ainda precisa conferir fontes, conclusões, direitos de imagem e aderência ao objetivo.

## Exemplo da devolutiva à equipe

> Podemos propor pautas sobre a oferta confirmada. Ainda não podemos fechar o visual: o feed acessível mostra duas paletas e falta o manual vigente. Consultamos o perfil e as três peças recebidas; isso não resolveu a divergência. Precisamos do PDF atual ou da indicação de qual peça representa a marca hoje. Responsável sugerido: atendimento/cliente. Enquanto isso, concluiremos o inventário e a estrutura das copys.

## Atualização contínua

Depois de cada pesquisa, feedback, aprovação ou medição, registrar a evidência, atualizar os campos afetados e gerar os relatórios. Manter “observado”, “hipótese” e “aprovado” distintos. Feedback de uma peça pode virar regra específica do cliente se confirmado para esse escopo; não vira regra para toda a agência.

Para retomar: “Leia a base do cliente em [pasta], confira LACUNAS.md e as decisões mais recentes e continue [missão]. Preserve a versão aprovada.” O PDF original do Studio continua sendo a introdução de vídeo/design; este guia é a entrada da camada nova de pesquisa e dossiês.

## Comparar uma amostra sem inventar viralização

Salve na base privada um JSON com period: {start, end} em datas ISO e posts: lista de observações. Cada post contém id, account, format, metric (uma só por registro), value (número ou null), locator (origem), published_at, collected_at, phase, paid e collab (booleano ou null). Duplicar um post para analisar outra métrica requer ID próprio. Datas seguem AAAA-MM-DD.

~~~bash
python scripts/benchmark.py projetos/clientes/clinica-exemplo/pesquisa/amostra.json --saida projetos/clientes/clinica-exemplo/pesquisa/comparacao-v1.json
~~~

A saída é criada sem sobrescrever um arquivo existente. Defina --minimo se a missão justificar outra convenção de tamanho; explique o limite da amostra. O script não compara curtidas a plays, não substitui mediana por seguidores e mantém fontes e exclusões. A mediana inclui os posts válidos fornecidos no grupo, não uma população presumida. A coleta e a seleção precisam estar documentadas na rodada de pesquisa. Não interprete um multiplicador descritivo como comprovação de viralização.

## Base já existente no Norteia

Consultar docs/NORTEIA.md antes de recadastrar manualmente. O preparador cria fontes e hipóteses em pastas privadas, sem pesquisar todos os perfis nem aprovar identidade. Ler também as bases privadas anteriores da cliente antes de usar o conteúdo importado.

## Conferência antes de entregar

~~~bash
python scripts/qualidade.py contraste --frente "#40352E" --fundo "#F5F1EA"
python scripts/qualidade.py copy projetos/clientes/cliente/producao/comparacao-copy.json
~~~

O JSON de comparação contém reference e output como textos. Use a copy de conteúdo, separada de cabeçalhos/assinaturas adicionais. O resultado 2 indica diferença a revisar ou contraste abaixo da meta; não faz correção automática. Os limites e fontes estão em references/aprimoramentos-instagram.md. Ver a arte no tamanho final continua necessário.
