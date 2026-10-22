# Critérios de pesquisa e criação · revisão de 22/10/2026

Este complemento ajusta o uso dos pacotes originais ao contexto de clientes da agência. As skills de terceiros permanecem com autoria e licença; suas fórmulas não substituem o objetivo, a voz e os dados do cliente.

## Pesquisa que muda a criação

Escolha as perguntas antes das fontes: o que precisamos saber para decidir pauta, argumento, prova, formato e CTA? Separe a observação da interpretação e da recomendação. Procure contraexemplos e conflitos; registre por que uma fonte foi excluída. Ao concluir, cada recomendação importante deve apontar as evidências que a sustentam e o próximo teste possível. É uma aplicação à criação da distinção entre observação e achado descrita pelo [GOV.UK Service Manual](https://www.gov.uk/service-manual/user-research/analyse-a-research-session).

O Norteia oferece contexto recebido da equipe, não prova de desempenho nem pesquisa externa concluída. Consulte [integração de leitura](../docs/NORTEIA.md). Não transfira uma identidade inteira porque dois clientes atuam no mesmo segmento.

## Instagram: contexto da conta antes de receitas universais

A Meta descreve seu hub de boas práticas com orientações gerais e dicas personalizadas por conta, cobrindo criação, engajamento, alcance e outras áreas. Quando o acesso permitir, consulte esse painel como fonte adicional e registre a data; não transforme a recomendação de uma conta em regra para as demais. Fonte: [anúncio oficial do hub, 2024](https://about.fb.com/news/2024/10/best-practices-education-hub-creators-instagram/).

A Meta também documentou a valorização do conteúdo original e a distinção de republicações em recomendações. Na adaptação, aproveite o mecanismo narrativo com argumento, provas e imagens próprios do cliente. A fonte é histórica e não comprova as condições exatas de distribuição atuais: [comunicado oficial, 2024](https://about.fb.com/ltam/news/2024/05/ayudando-a-los-creadores-a-encontrar-nuevas-audiencias/). Não prometa alcance porque uma peça parece seguir o comunicado.

Os pacotes incluídos contêm contagens de caracteres, fórmulas e afirmações sobre algoritmo e pontuação de perfil. Trate como heurísticas; confirme especificações atuais quando forem decisivas. Pontuação editorial não estima conversão. Não diga que sabe por que um post performou só porque reconheceu o gancho.

## Voz em português e revisão de copy

Escolha exemplos reais da marca e procure ritmo, grau de formalidade, palavras, maneiras de explicar e limites de humor. Não impor ao português as listas inglesas do humanizer. Evitar detector de “texto de IA” como critério de qualidade. Não prometer remover marca d'água de modelo por substituir palavras ou pontuação.

Um humanizador pode sugerir mudanças, mas deve preservar fatos, ressalvas, números, unidades e significado. Não remover caracteres invisíveis, conectivos ou pontuação cegamente; podem fazer parte da formatação ou de símbolos. Quando o pedido for apenas visual, comparar a copy de referência e o texto do editor. O helper scripts/qualidade.py copy identifica diferenças ignorando apenas espaços e normalização Unicode; a revisão decide se a mudança foi autorizada.

## Contraste com acabamento

A [W3C](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) usa referências de 4,5:1 para texto e 3:1 para texto grande, conforme suas definições, e alerta que traços finos podem parecer mais fracos mesmo quando o par de cores passa. A aplicação a um carrossel é um auxílio de leitura: tamanho no arquivo 1080 px não demonstra tamanho percebido no celular, nem conformidade WCAG da publicação inteira.

Use scripts/qualidade.py contraste para testar cores sólidas. Em foto ou textura, examine o fundo em toda a região ocupada pelas letras e confira a prévia reduzida. Se houver texto fino bege/marrom com pouca leitura, mudar contraste, peso ou escala antes de acrescentar sombra. O cálculo não detecta recorte, palavras quebradas, imagem sem relação ou fio atravessando uma frase; revisar cada página.

## Melhorar a partir do resultado

Use templates/cliente/experimento.md. Vincule a peça a um objetivo comercial, uma hipótese e uma medida possível. Defina antes como observar o resultado e qual decisão ele mudará. Quando comparar peças, registrar público, formato, distribuição, janela e alterações relevantes; sem desenho adequado, falar em associação e teste exploratório, não em causalidade.

Após publicar com autorização própria, anotar resultados reais e feedback da equipe. Atualizar somente as conclusões sustentadas. Nenhum template torna uma promessa comercial verdadeira ou transforma uma preferência estética em evidência de venda.
