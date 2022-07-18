> # Questão 3 - Relatório
> (4 pontos) **Relatório**: construa um relatório utilizando o Markdown para escrever. Seja criativo para apresentar seus achados e siga os passos abaixo:
>    * Imagine que você possui uma startup e este é o primeiro relatório apresentará
>    * Coloque o nome do seu produto
>    * Apresente a introdução do problema (seja sucinto, escreva com poucas palavras)
>    * Coloque gráficos e frases para sustentar seus argumentos
>    * Mostre as soluções do mercado
>    * Escreva sobre a sua solução e por que ela é a melhor

# WYNER - Sistema de Recomendação de Vinhos

![Nuvem de palavras mais comuns para se referir aos vinhos](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/wines_description_wordcloud.png?raw=true "Nuvem de palavras mais comuns para se referir aos vinhos")

## Link de acesso ao aplicatiVO WYNER

https://tinyurl.com/4kztht79

## Introdução

Escolher um bom vinho para uma determinada ocasião pode ser uma tarefa difícil. Qual o melhor vinho para aquele jantar romântico? Qual combina com peixe? Espumante ou não? São tantas as possibilidades e variedades diferentes que é difícil escolher. Você pode consultar o sommelier e ele certamente lhe indicara o melhor vinho que ele conhece. Mas mesmo um bom sommelier não é capaz de conhecer toda a variedade de vinhos existente. Além de que não é fácil nem barato encontrar um bom sommelier a sua disposição.

Pensado em resolver este problema criamos o WYNER. WYNER conta com uma base de dados de mais de 100.000 títulos diferentes de vinhos. Este sistema consulta as avaliações dadas por alguns dos melhores sommeliers do mundo e pode lhe recomendar o vinho ideal. Com apenas alguns cliques o usuário têm a sua disposição a lista de alguns dos vinhos mais renomados que atenderão seus desejos.
 
## 2. Apresentação do WYNER

WYNER é um sistema de recomendação de vinhos. Este sistema utiliza a descrição de diversos títulos de vinhos para realizar a recomendação dos vinhos mais semelhantes entre si. A base de dados do WYNER conta com 117.236 títulos diferentes.

O usuário pode filtrar o conteúdo através dos atributos: país de origem (`country`), nota de avaliação (`points`), preço sugerido (`price`), estilo de vinho (`style`). 

![tela principal do WYNER](https://i.imgur.com/k07RHdW.png "Tela principal do WYNER")

Após o usuário selecionar um vinho do catálogo o sistema retorna uma lista com os 10 títulos cujas descrições mais se assemelham à descrição do vinho selecionado.

![Lista de vinhos](https://imgur.com/CUmMlNZ.png "Lista de vinhos")

A semelhança entre as descrições é calculada utilizando a combinação do `CountVectorizer` (para extração de características) e o KNN (para o cálculo da semelhança de acordo com as características extraídas).

### 3. Porquê utilizar o WYNER

O WYNER é uma forma inteligente de encontrar um bom vinho. Sua base diversa de dados contém vinhos com sabores que agradam a todos os paladares. Dificilmente o usuário não encontrará uma recomendação que lhe agrade. É um sistema simples de utilizar e estará a disposição do usuário 24 horas por dia, bem diferente de um sommelier convencional. 

Em uma versão futura integraremos o WYNER com lojas especializadas. Ao selecionar um título em nosso sistema ele já será adicionado ao carrinho de compras na loja parceira. E restará ao usuário apenas a tarefa e efetivar a comprar e aguardar a entrega em sua residência.

### 4. Descrição da base de dados

A base de dados inicial do WYNER conta com 117.236 títulos de vinhos diferentes oriundos de 43 países. Os 10 principais países produtores da base são exibidos no gráfico a seguir.
![Países mais comuns do dataset](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/top_10_coutries_by_production.jpeg?raw=true "Países mais comuns do dataset")

Contamos com vinhos dos principais estilos distribuídos conforme o gráfico abaixo. A base tem predominância de vinhos tintos e brancos devido a sua alta popularidade.
![Distribuição dos estilos de vinhos do dataset](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/most_common_wine_styles.png?raw=true "Distribuição dos vinhos do dataset por estilo")

A sistema de avaliação utilizado permite notas entre 0 e 100 pontos. Mas apenas vinhos com nota igual ou superior a 80 pontos foram selecionados. isto garante um alto padrão de qualidade em nossa base de dados.
![Distribuição das notas dos vinhos](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/hist_wine_points.png?raw=true "Distribuição das notas dos vinhos")

Os preços também variam bastante. Temos vinhos entre U$S 4,00 e U$S 3.300,00 para agradar a todos os bolsos. E mesmo os vinhos mais baratos são muito bem avaliados.
![Distribuição dos preços dos vinhos](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/hist_wine_prices.png?raw=true "Distribuição dos preços dos vinhos")

### 5. Soluções de mercado

Com certeza temos fortes concorrentes de mercado como o **Vivino** que hoje conta com uma base de milhões de avaliações. Porém nossa base inicial é bastante diversificada já que iniciamos com mais de 100.000 títulos únicos. Após entramos em produção poderemos permitir a inclusão de avaliações de forma colaborativa o que expandirá nossa base de dados e melhorar as recomendações feitas. Temos um sistema dinâmico que poderá ir se adaptando e evoluindo com o tempo. Focaremos em entregar a melhor recomendação possível aos nossos usuários sempre.
