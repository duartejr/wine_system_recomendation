# WYNER - Sistema de Recomendação de Vinhos


### 1. Descrição
WYNER é um sistema de recomendação de vinhos. Este sistema utiliza a descrição de diversos títulos de vinhos para realizar a recomendação dos vinhos mais semelhantes entre si. A base de dados do WYNER conta com 117236 títulos diferentes.

O usuário pode filtrar o conteúdo através dos atributos: país de origem (`country`), nota de avaliação (`points`), preço sugerido (`price`), estilo de vinho (`style`). Após o usuário selecionar um vinho do catálogo o sistema retorna uma lista com os 10 cujas descrições mais se assemelham à descrição do vinho selecionado. 

A semelhança entre as descrições é calculada utilizando a combinação do `CountVectorizer` (para extração de características) e o KNN (para o cálculo da semelhança de acordo com as características extraídas). 

A seguir é explicado o processo de análise da base de dados original (**2. Análise Exploratória**), a modelagem do sistema de recomendação (**3. Sistema de Recomendação**) e um manual de uso do aplicativo beta criado (**4. Aplicativo**).

### 2. Análise Exploratória

#### 2.1 Base de dados
A base de dados utilizadas foi o dataset de revisões de vinhos de Zackthout disponível publicamente no [Kaggle](https://www.kaggle.com/datasets/zynicide/wine-reviews). Este dataset contém o registro de 13000 avaliações de vinhos feitas por diversos especialistas.
O dataset contém as seguintes variáveis
| Variável | Descrição |
| -- | -- |
| Unnamed: 0 | Identificador único para cada avaliação. |
| country | O país onde o vinho foi produzido. |
| description | Descrição do vinho segundo o especialista que o avaliou. |
| designation | A vinha de onde são provenientes as uvas do vinho. |
| points | O número de pontos que a WineEnthusiast avaliou o vinho em uma escala de 1 a 100 (embora eles digam que só postam avaliações para vinhos com pontuação >=80) |
| price | O preço de uma garrafa de vinho. |
| province | A província ou estado onde o vinho foi produzido. |
| region_1 | A área de vinicultura de uma província ou estado. |
| region_2 | Região mais específica fornecida para alguns vinhos. |
| taster_name | Responsável pela avaliação do vinho. |
| taster_twitter_handle | Perfil do Twitter do avaliador. |
| title | O título da avaliação do vinho, que geralmente contém a safra. |
| variety | O tipo de uvas utilizadas para produzir o vinho. |
| winery | A vinícula que produziu o vinho. |

#### 2.2 Tratamento de valores nulos

Na base de dados original foram encontradas os seguintes registro de valores nulos.

| Variável | Quantidade de nulos | Percentual de nulos | 
| -- | -- | -- |
| Unnamed: 0 | 0 | 0.00 % |
| country | 63 | 0.05 % |
| description | 0 | 0.00 % |
| designation | 37465 | 28.83 % |
| points | 0 | 0.00 % |
| price | 8996 | 6.92 % |
| province | 63 | 0.05 % |
| region_1 | 21247 | 16.35 % |
| region_2 | 79460 | 61.14 % |
| taster_name | 26244 | 20.19 % |
| taster_twitter_handle | 31213 | 24.02 % |
| title | 0 | 0.00 % |
| variety | 1 | 0.00 % |
| winery | 0 | 0.00 % |

As colunas `Unnamed:0 `, `designation`, `region_1` e `region_2` foram removidas da base de dados do modelo de recomendação. Pois, estas variáveis além de terem um quantitativo expressivo de falhas e inviabilidade para preenchimento das mesmas não apresentam informação relevante para o modelo de recomendação.

Foram removidos os registros que não tinham informação do país de origem e da variedade de uvas utilizada para a produção do vinho. As falhas na coluna de preços foram preenchidas com o valor médio dos preços, já que o quantitativo de falhas nesta coluna não é tão expressivo apenas 6.92%.

As duas colunas referentes aos avaliadores também foram removidas da base de dados utilizada para alimentar o sistema de recomendação.

#### 2.2 Tratamento de dados duplicados

Foram encontrados no dataset um total de 9979 registros duplicados. Como as informações duplicadas não agregam para o sistema de recomendação estes registros foram removidos. Após esta fase sobraram 119929 registros.

#### 2.3 Insights

Nesta seção são descritos alguns insights obtidos a partir da análise dos dados.

##### 2.3.1 Qual o vinho mais caro?

O vinho mais caro do dataset é o Château les Ormes Sorbet 2013 Médoc. Este vinho é produzido na província de Bordeaux na França. Ele têm um preço de U$S 3300.00 e avaliação de 88 pontos. Ele é produzida com uvas da variedade Bordeaux pela vinícola Château les Ormes Sorbet.

##### 2.3.2 Qual o vinho mais barato?

O vinho mais barato do dataset é o Bandit NV Chardonnay (California). Ele é produzido na Califórina nos Estados Unidos. Têm um preço sugerido de U$S 4.00 e sua avaliação é de 86 pontos. A variedade de uvas utilizada é a Merlot e a vinícola é a Bandit.

##### 2.3.3 Qual o especialista avaliou mais vinhos?

O especialista com a maior quantidade de registros avaliados no dataset é o Roger Voss. Ele avaliou um total de 23558 títulos dando uma nota média de 88.73.

##### 2.3.4 Qual a região possui os vinhos com a melhor média de avaliação?

A província de Südburgenland na Áustria têm a melhor avaliação média, 94 pontos. Nela são produzidos dois vinhos o Jalits e o Krutzler. Ambos são vinhos tintos e a safra avaliada foi a de 2012.

##### 2.3.5 Qual a província têm os vinhos com a menor média de preços?

Os vinhos produzidos em Viile Timisului na Romênia têm a menor média de preços. Contudo no dataset consta apenas um único exemplar de vinho produzido nesta região que é o Cramele Recas de 2014 cujo preço sugerido é de U$S 7.00.

##### 2.3.6 Quais os vinhos com as melhores e piores avaliações?

Os 5 vinhos mais bem avaliados (todos com nota máxima) são: Quint do Noval (2011), Charles Simth (2006), Casa Ferreirinha (2008), Csanova di Neri (2007), Cardinale (2006).
Os vinhos com piores avaliações (todos com nota de 80) são: Cooper Vineyards NV, Finca Pasion (2009), Maddalena (2010), Corinto (2009), Campus Oaks (2012).

##### 2.3.7 Qual a distribuição das avaliações? Quantas avaliações um vinho recebe?

Observando o histograma abaixo se percebe que a maioria dos vinhos têm apenas uma única avaliação. Isto pode ser um fator que possa gerar uma avaliação enviesada do modelo.
![histograma da distribuição das avaliações](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/hist_wine_evaluations.png?raw=true "Histograma do número de avaliações por vinho")

##### 2.3.8 Distribuição espacial dos registros.

O dataset possui o registro de 43 países. Os 10 países com maior quantidade de vinhos registrada é exibido no gráfico abaixo. França e Itália conhecidas por produzirem vinhos de excelente qualidade ocupam a 2ª e 3ª posição respectivamente, ficando atrás dos Estados Unidos. Como o dataset foi coletado de uma base americana é normal que existam mais registro para o referido país do que para os demais.
![Países mais comuns do dataset](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/top_10_coutries_by_production.jpeg?raw=true "Países mais comuns do dataset")

##### 2.3.9 Distribuição dos estilos de vinho

No seguinte site (https://winefolly.com/tips/the-9-major-wine-styles/) são listados os 9 principais estilos de vinho. Com base nesta informação os vinhos do dataset foram classificados de acordo seu estilo. Algumas vaiedades de vinhos foram classificadas a partir do site referido anteriormente e outras foram classificadas após extensa pesquisa na internet algumas fontes consultadas foram: vivino, wine.com, wineparadigm.com, virginwines, winefolly, winebody, vinello...

A seguir é exibida a distribuição dos vinhos mais comumns no dataset por estilo.
![Distribuição dos estilos de vinhos do dataset](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/most_common_wine_styles.png?raw=true "Distribuição dos vinhos do dataset por estilo")

Vinhos tintos (`Red`) são o estilo mais comum no dataset em seguida estão os brancos (`white`). Quanto a subcategoria os tintos encorpados (`full-bodied red wines`) estão são os que têm a maior quantidade de títulos no dataset e em seguida estão os Brancos secos (`Light-Bodied White Wines`). Vinhos do tipo Rosé e espumantes são os estilos com a menor quantidade de títulos registrada.

##### 2.3.10 Distribuição dos preços dos vinhos

Os preços de vinhos variam entre U$S 4.00 e U$S 3300.00. Porém a distribuição não é uniforme com a maioria dos preços concentrada abaixo dos U$S 100.00. Para poder visualizar melhor a distribuição dos preços (gráfico abaixo) foi utilizada a escala logarítmica no eixo X. O pico apresentado no gráfico corresponde a preços em torno de U$S 35.00.
![Distribuição dos preços dos vinhos](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/hist_wine_prices.png?raw=true "Distribuição dos preços dos vinhos")

##### 2.3.11 Distribuição das notas dos vinhos

As notas dos vinhos variam entre 80 e 100 pontos com mediana aproximada de 88 pontos. As notas são dadas em um intervalo discreto, apenas valores inteiros são utilizados como nota. Aparentemente a distribuição das notas se adéqua bem a uma distribuição normal, o que indica que pode não haver um viés de avaliação no conjunto de dados. Média e media estão bem próximas de 88 pontos.
![Distribuição das notas dos vinhos](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/hist_wine_points.png?raw=true "Distribuição das notas dos vinhos")

Considerando-se a mediana dos boxplots apresentados na figura a seguir os vinhos "Light-Bodied Rede Wines" tendem a ter melhores avaliações que os demais. E os "Rosé Wines" têm a menor mediana de avaliações. Em geral os vinhos tinto costumam ter melhores avaliações que os vinhos brancos.
![Distribuição das notas por estilo de vinho](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/boxplot_wine_points_by_style.png?raw=true "Distribuição das notas por estilo de vinho")

##### 2.3.12 Quais os adjetivos mais comuns utilizados pelos avaliadores?

A nuvem de palavras a seguir ilustra alguns dos termos mais utilizados pelos avaliadores para se referir aos vinhos avaliados. Full bodi, refere-se aos estilos dos vinhos como observado pelas análises anteriores os vinhos com estilo "full-bodied" tanto tintos quanto brancos são os mais comuns do dataset por isto é esperado que este seja um dos termos mais comuns. Sabores relacionados a frutas (fruit flavor, black fruit, black cherri) também são destaque em especial porque a maioria dos vinhos é do tipo tinto. carbernet Sauvignon é uma das variedades de uvas mais utilizadas na produção de vinhos.
![Nuvem de palavras mais comuns para se referir aos vinhos](https://github.com/duartejr/wine_system_recomendation/blob/main/data/output_images/wines_description_wordcloud.png?raw=true "Nuvem de palavras mais comuns para se referir aos vinhos")

### 3. Sistema de Recomendação

Para o sistema de recomendação foram testados dos métodos para a extração de características das descrições dos vinhos: Tfidf Vectorizer e Count Vectorizer. Foi realizado um preprocessamento nos textos para remoção de stopwords, pontuação e sufixos das palavras. Para o cálculo da similaridade entre os textos foi utilizado o método de KNN tendo a distância cosseno como métrica de semelhança.

#### 3.1 Pré-processamento das descrições

Foram removidos da base de dados todos os títulos que não foram classificados em um dos estilos de vinho ficando um total de 117.236 registros. Os textos das descrições foram normalizados para que todas as palavras ficassem e minúsculas. Utilizou-se o pacote NLTK para realizar a criação de tokens e remoção de pontuação. Foi utilizada a lista de stopwords do NLTK. E o `PorterStemmer` para realizar a remoção de sufixos das palavras. O dataset foi dividido em duas partes a primeira `wines_recomendation_system.csv` contém apenas os títulos e a descrição dos mesmos preprocessada e é utilizada como input do algoritmo de recomendação. A segunda `wines_user_consul.csv` contém o título, a descrição original, país, província, nota, preço, variedade, vinícola e estilo do vinho; esta será a base de dados a qual o usuário interagirá.

#### 3.2 Algoritmos de recomendação

#### 3.2.1 Tfif Vectorizer

### 4. Aplicativo

