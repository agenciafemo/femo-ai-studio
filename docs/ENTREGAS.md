# O que criar a partir da base do cliente

A base reúne conhecimento de marca e negócio para alimentar diferentes trabalhos, além da pesquisa de Instagram. O mesmo contexto pode orientar key visual, briefing, Reels, carrosséis, stories, campanhas, anúncios, páginas, apresentações e planos editoriais.

## Peça em linguagem natural

> Leia a base do cliente [pasta]. Use o objetivo e as decisões vigentes para criar [entrega], sobre [tema]. Selecione as evidências relevantes, desenvolva a proposta e indique as dependências específicas. Não reinicie a identidade nem peça novamente informações já fornecidas.

Exemplos:

- “Crie o conceito e o key visual desta campanha, com peça principal e desdobramentos em feed e stories.”
- “Transforme a pesquisa em um briefing para o designer, com mensagem, prova, referências e critérios de avaliação.”
- “Monte o direcionamento de Reels: fala, cenas, imagens de apoio e instruções de gravação para a cliente.”
- “Escreva o carrossel com progressão, copy por slide e legenda; depois proponha a direção artística.”
- “Use as objeções e provas da base para estruturar a página desta oferta.”

## Preparação local opcional

A IA pode usar o helper para selecionar a base e registrar o briefing do pedido:

~~~bash
python scripts/entregas.py tipos
python scripts/entregas.py preparar projetos/clientes/cliente --tipo key-visual --tema "Campanha de lançamento" --pedido "Conceito, peça principal e dois desdobramentos"
python scripts/entregas.py preparar projetos/clientes/cliente --tipo reels --tema "Dúvida recorrente do público" --pedido "Direção de gravação e roteiro"
~~~

Os arquivos CONTEXTO.json e BRIEFING.md ficam em uma nova pasta de producao/ do cliente. O dossiê permanece intacto. Esse comando prepara contexto; não produz imagem, vídeo ou copy final automaticamente. Depois, a IA desenvolve a entrega conforme o pedido e as ferramentas disponíveis.

Os dez tipos estão em templates/entregas/catalogo.json. Cada um seleciona campos necessários e complementares, perguntas da peça e critérios de conclusão. A seleção pode ser adaptada ao escopo; o catálogo não obriga a criar todos os formatos.

## Lacunas proporcionais à entrega

Não exigir as mesmas informações para tudo. Identidade visual é central para fechar um key visual; para a copy de carrossel, voz e argumento podem permitir começar antes da arte. Reels precisa considerar gravação ou brutos existentes. Uma campanha requer coerência entre oferta, canais e operação.

required_context_ready no JSON indica apenas que os campos exigidos pelo tipo passaram na checagem estrutural. Não comprova qualidade, adequação de uma promessa, disponibilidade dos ativos ou aprovação humana. Informações específicas da peça ainda devem ser conferidas no pedido e nos arquivos.

As lacunas indicam onde falta fonte, confirmação, revisão ou resolução de conflito. Um rascunho exploratório autorizado pode avançar com hipóteses identificadas. Uma entrega final não pode simular dependências resolvidas.

Leia [o método de criação por entrega](../references/entregas-criativas.md). Para um cliente já cadastrado no Norteia, aproveite a base privada preparada; esse fluxo não grava no app nem publica conteúdos por conta própria.
