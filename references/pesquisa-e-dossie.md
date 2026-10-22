# Pesquisa com evidências e base do cliente

## Contrato da rodada

Leia o dossiê existente, suas decisões aprovadas e a missão atual. Informe o objetivo comercial em uma frase, a entrega pretendida, o período analisado e o acesso real. Um pedido de estudo termina em estudo; produção começa quando solicitada. Não herde paleta, imagens, tom ou regras de assinatura de outro cliente.

Use scripts/clientes.py para abrir a estrutura, registrar evidências e verificar lacunas. O JSON é o registro estruturado; DOSSIÊ.md e LACUNAS.md são visões geradas dele. Notas extensas e arquivos originais ficam nas subpastas indicadas em docs/CLIENTES.md. Não edite apenas a visão gerada esperando atualizar o JSON.

## Equipe de pesquisa

Use os [contratos portáteis de tarefa](../agents/pesquisa.md) para entregar o contexto mínimo a cada agente.

São papéis de trabalho com contratos definidos, não contas conectadas ou serviços em execução. Quando o usuário autorizar agentes e o ambiente oferecer delegação, o coordenador pode distribuir os papéis independentes abaixo. Sem isso, execute os mesmos papéis em sequência e informe o modo real. Não invente agentes, navegação ou resultados.

| Papel | Investigar | Entrega obrigatória |
| --- | --- | --- |
| Contexto e estratégia | Site, oferta, briefing, público, diferenciais, conversão e objetivo | Fatos com fontes; hipóteses de público separadas; perguntas que só a equipe pode responder |
| Perfil e conteúdo próprio | Bio, links, destaques acessíveis, fixados, grade e posts completos | Inventário datado, amostra, limites de leitura, padrões positivos e negativos, provas disponíveis |
| Referências e desempenho | Concorrentes diretos e referências de linguagem; conteúdos fortes e fracos | Perfis justificados, posts com links, métrica e comparação válida, mecanismo adaptável e limites |
| Identidade e voz | Manual atual, peças aprovadas, fotografias, carrosséis e falas da marca | Sistema visual observado, exemplos reais de voz, conflitos entre versões, regras confirmadas e propostas |
| Síntese e revisão | Cruzamento de todas as entregas | Dossiê, mapa de evidências, contradições, lacunas priorizadas e plano de conteúdo coerente com o objetivo |

Cada papel recebe: cliente e objetivo, escopo e período, caminhos permitidos, IDs reservados (ex.: PERF-001), fontes já conhecidas e perguntas. Devolve arquivo próprio em pesquisa/, evidências candidatas e limitações. Só o coordenador incorpora ao dossie.json; agentes não editam simultaneamente esse arquivo. Não compartilhe credenciais com agentes.

## Investigar o Instagram de verdade

1. Identifique o perfil por URL e confirme sua relação com a marca. Inspecione o que está disponível no navegador/conector da sessão; não prometa que um link permite ler tudo.
2. Abra posts para ler a sequência, legenda e, em Reels, o início e desenvolvimento. Uma capa na grade não permite avaliar todo o carrossel. Registre exatamente o que foi visto: capa, sequência completa, trecho de vídeo ou legenda.
3. Se houver login pendente, peça que a equipe entre no navegador e continue pesquisa pública independente. Não peça senha. Se o acesso continuar bloqueado, registre tentativa e solicite exportações/capturas específicas. Não contorne bloqueios.
4. Apify é opcional: o pacote terceiro contém o cliente e as skills de leitura, mas conta, créditos, token e autorização de consumo são requisitos reais. Não executar coleta paga por dedução. Dados fornecidos pela equipe também são válidos, com origem identificada.
5. Defina amostragem antes de selecionar destaques: por exemplo, todos os posts de um período recente acessível, mais fixados e campanhas pertinentes. É um ponto de partida ajustável ao volume, não cota universal. Registre total visto, exclusões e motivos. Explore referências além dos perfis já conhecidos e justifique cada inclusão por público, oferta ou linguagem.
6. Compare o período completo com os destaques para evitar escolher apenas sucessos. Abra também exemplos abaixo da linha de base. Separe fases de rebranding e collabs quando mudarem a leitura.
7. Pare quando a amostra sustentou as decisões da missão ou quando novas tentativas não acrescentarem evidência. Conteúdo viral de ontem não garante desempenho amanhã. Declare cobertura parcial e pendências; nunca chame uma grade vista de varredura completa.

## O que conta como evidência

Cada registro em evidence tem ID estável, URL/caminho local preciso, tipo, data da coleta (ISO), nível de acesso e uma observação verificável. Inclua autor/conta e data da publicação quando disponíveis. Para métrica, use nome, valor, unidade e instante da observação. Ausente ou oculto é null, nunca zero. Captura local deve conservar contexto suficiente para localizar a origem.

Separe três camadas nas notas: observação (o que a fonte mostra), interpretação (o que isso sugere) e proposta (o que testar). Se concluir que há um padrão, cite mais de uma ocorrência e procure contraexemplos; uma peça pode ser inspiração, sem provar padrão. Não deduza renda, idade exata, condição médica ou intenção de compra de uma foto ou comentário.

Para cada referência visual: link/captura + característica observada + elemento aproveitável + o que não copiar. A licença de uma skill não concede direitos sobre fotos, logos ou posts analisados. Não reproduza textos completos de terceiros no pacote público.

## Desempenho e alegação de viral

Use a mesma métrica em peças comparáveis e declare período, tamanho da amostra e idade dos posts. Preferir comparação dentro da própria conta por formato e contexto: valor do post / mediana dos posts comparáveis. Se a mediana for zero, a amostra for pequena ou as contagens estiverem ocultas, não invente multiplicador. Declare insuficiência.

Curtidas e comentários públicos não equivalem a alcance, salvamentos, compartilhamentos, leads ou vendas. Número de seguidores é contexto, não alcance comprovado. Plays de Reels não são comparáveis diretamente a curtidas de carrosséis. Misturar likes+comentários só é aceitável como índice nomeado, com as mesmas componentes em todos os itens.

Registre anúncios conhecidos, collabs, fixados, datas e campanhas como possíveis fatores de confusão. Uma associação não explica causalmente o sucesso. Sem baseline ou Insights fornecidos, use “referência encontrada” ou “alto número observado”, não “viral comprovado”. Sem dados privados não prometa conversão. Não invente horários ideais, regras do algoritmo ou limites atuais da plataforma; confira fontes oficiais quando isso mudar a decisão.

## Síntese e lacunas

Verifique o dossiê antes de criar: python scripts/clientes.py verificar projetos/clientes/cliente --etapa design. O relatório automático confere estrutura, estado, fontes e validade temporal configurada; não comprova verdade, qualidade da pesquisa nem aprovação humana.

Para cada lacuna informe: item exato, impacto na entrega, o que já foi consultado, fonte/pergunta concreta e responsável sugerido. Agrupe perguntas para a equipe. Continue apenas nas partes independentes; identidade indefinida bloqueia aplicação final da marca, mas não impede inventário ou rascunho de argumento. Uma peça experimental autorizada pode avançar com hipótese explicitada, sem promovê-la a regra aprovada.

Conflitos entre manual antigo, feed e orientação recente devem ser registrados e resolvidos com fonte datada. Não “corrija” silenciosamente uma versão aprovada. Um campo confirmado sem fonte, expirado ou em conflito volta a ser pendência na etapa que dele depende.

## Alimentar a base

Ao receber material, feedback ou resultados: registre fonte → atualize o campo ou decisão com histórico → reavalie conflitos → gere os relatórios → resuma o que mudou. Preservar versões aprovadas e feedback recusado com motivo. Não transfira uma preferência visual de um cliente aos demais.

Ao encerrar uma produção, registre objetivo da peça, copy vigente, direção por página, imagens e direitos, link editável, versão, estado (proposta/aprovada/salva/publicada) e referência à aprovação. Publicada exige evidência própria. Incorpore desempenho apenas depois de existir medição datada; mantenha o aprendizado como hipótese enquanto faltar teste.
