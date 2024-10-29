# Projeto de Expansão Airbnb - Análise de Dados de Imóveis em Nova York

Este projeto visa explorar e analisar dados de listagens do Airbnb em Nova York, utilizando ciência de dados e visualização para extrair insights sobre preços, tipos de acomodações e distribuição geográfica. O objetivo é identificar regiões promissoras para a aquisição de imóveis que ofereçam alta rentabilidade para a empresa, apoiando a expansão do Airbnb em locais estratégicos.

## Descrição do Projeto

O projeto utiliza o conjunto de dados **New York City Airbnb Open Data**, disponível no [Kaggle](https://kaggle.com), para 2019. As análises são parte do curso "Python para Ciências de Dados" da Comunidade DS e utilizam técnicas de aprendizado supervisionado para explorar e entender as tendências e padrões nos dados de listagens do Airbnb.

### Objetivo
O objetivo principal deste projeto é identificar as melhores regiões em Nova York para a compra de imóveis, considerando fatores como preço médio de aluguel, tipo de acomodação e popularidade (número de avaliações) para otimizar as decisões de investimento e maximizar a rentabilidade.

### Estrutura dos Dados
O conjunto de dados contém as seguintes colunas principais:
- **id**: Identificador único da listagem.
- **host_id**: Identificador único do anfitrião.
- **name**: Nome do anúncio ou propriedade.
- **host_name**: Nome do anfitrião.
- **neighbourhood_group**: Região geral da propriedade (ex: Manhattan, Brooklyn).
- **neighbourhood**: Bairro específico.
- **latitude** e **longitude**: Coordenadas geográficas.
- **room_type**: Tipo de acomodação (quarto privado, apartamento inteiro, etc.).
- **price**: Preço da diária.
- **minimum_nights**: Número mínimo de noites para reserva.
- **number_of_reviews**: Total de avaliações da propriedade.
- **last_review**: Data da última avaliação.
- **reviews_per_month**: Média de avaliações por mês.
- **calculated_host_listings_count**: Contagem calculada de listagens por anfitrião.
- **availability_365**: Disponibilidade da listagem ao longo do ano.

### Questões de Negócio
O Airbnb pretende identificar as melhores oportunidades de compra de imóveis em Nova York. Para isso, foram levantadas questões como:
- Quais regiões possuem o maior número de acomodações com alta rentabilidade?
- Qual é o preço médio de aluguel por região?
- Quais são os tipos de acomodações mais populares e como isso impacta a rentabilidade?
- Quais propriedades recebem mais avaliações, indicando maior popularidade?

### Insights Obtidos
Com base nas análises, os seguintes insights foram identificados:
1. **Preço Médio**: O preço médio de aluguel é de aproximadamente U$152,72, com um desvio padrão de U$240,15, indicando uma variação considerável nos preços.
2. **Regiões Populares**: As regiões com maior rentabilidade incluem Brooklyn, Manhattan e Queens, onde os preços de aluguel e a demanda são mais elevados.
3. **Acomodações Acessíveis**: Existem mais de 2.000 acomodações com valor de aluguel até U$100, sugerindo uma oferta significativa de acomodações acessíveis.
4. **Interação com Avaliações**: Cerca de 30.000 imóveis possuem menos de 10 avaliações, o que pode indicar baixa visibilidade ou imóveis recém-listados.

### Ferramentas Utilizadas
- **Python** (versão 3.10)
- **Bibliotecas**: `pandas`, `numpy`, `plotly`, `folium`, `matplotlib`
- **IDEs**: PyCharm, VSCode, Google Colab
- **Controle de Versão**: Git e GitHub

---

## Guia do Código

O código é dividido em seções para facilitar a compreensão e a análise dos dados. Abaixo estão os detalhes:

## 1. Carregamento dos Dados

Carregamos o conjunto de dados utilizando `pandas`, e verificamos as primeiras linhas para assegurar que os dados foram carregados corretamente.

```python
import pandas as pd
data = pd.read_csv('/content/AB_NYC_2019.csv')
data.head()


## 2. Análise Exploratória de Dados (EDA)

### 2.1 Análise dos Preços
Para entender a distribuição dos preços, calculamos a média e o desvio padrão da coluna `price`. Esses valores são importantes para identificar a faixa de preços e a variabilidade dos aluguéis em Nova York.

```python
import numpy as np
price = data['price']
valor_medio = np.mean(price)
desvio_padrao = np.std(price)
print(f'Preço médio: U$ {valor_medio:.2f}, Desvio padrão: U$ {desvio_padrao:.2f}')

### 2.2 Identificação das Regiões e Tipos de Acomodação
Para entender as categorias de localização e tipo de acomodação, extraímos as regiões únicas (`neighbourhood_group`) e os tipos de quarto (`room_type`). Isso permite identificar as principais áreas onde os imóveis estão localizados e as categorias de acomodação oferecidas.

```python
regioes_unicas = pd.unique(data['neighbourhood_group'])
room_type_unique = np.unique(data['room_type'])
print('Regiões:', regioes_unicas)
print('Tipos de Acomodação:', room_type_unique)

### 2.3 Análise de Frequência - Histograma

Para entender a distribuição dos preços e do número de avaliações, utilizamos histogramas. Esses gráficos mostram a frequência de imóveis em faixas de preços e a quantidade de avaliações, auxiliando na identificação de padrões e concentrações nas listagens.

- **Distribuição de Preços:** Filtramos os dados para imóveis com preços abaixo de U$1250, focando na distribuição dos valores mais comuns para aluguel.
- **Distribuição de Avaliações:** Analisamos imóveis com menos de 300 avaliações para verificar a popularidade e o engajamento das listagens.

```python
from matplotlib import pyplot as plt

# Histograma de Preços
filtered_price = data[data['price'] < 1250]['price']
plt.hist(filtered_price, bins=12)
plt.title("Distribuição de preços (até U$ 1250)")
plt.xlabel("Preço")
plt.ylabel("Frequência")
plt.show()

# Histograma de Avaliações
filtered_reviews = data[data['number_of_reviews'] < 300]['number_of_reviews']
plt.hist(filtered_reviews, bins=12)
plt.title("Distribuição do número de avaliações (até 300)")
plt.xlabel("Número de Avaliações")
plt.ylabel("Frequência")
plt.show()

## 3. Análise de Preço por Região - Gráfico de Barras

Para identificar as áreas com maior potencial de lucro, agrupamos os dados por `neighbourhood_group` e calculamos o preço máximo por região. Esse gráfico de barras facilita a visualização das diferenças de preços entre as regiões e destaca os bairros com as listagens de aluguel mais caras, o que pode ser útil na estratégia de compra de imóveis.

```python
import plotly.express as px

data_grouped = data.groupby('neighbourhood_group')['price'].max().reset_index()
px.bar(data_grouped, x='neighbourhood_group', y='price', title='Preço Máximo por Região')

## 4. Mapeamento de Imóveis - Folium

Utilizando a biblioteca `folium`, criamos um mapa interativo que mostra a localização dos imóveis com base em suas coordenadas de latitude e longitude. Essa visualização permite identificar a distribuição geográfica das listagens de maior valor, ajudando a destacar as áreas mais estratégicas para investimento.

Cada imóvel é marcado no mapa com um pino, e ao clicar em um pino, é possível ver informações detalhadas, como a região (`neighbourhood_group`) e o preço máximo de aluguel.

```python
import folium

# Definir o centro do mapa usando a média das coordenadas
mapa = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Adicionar marcadores ao mapa
for _, row in data_grouped.iterrows():
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=f"{row['neighbourhood_group']} - Preço Máximo: U${row['price']}",
        icon=folium.Icon(color='blue')
    ).add_to(mapa)

# Exibir o mapa
mapa

## 5. Visualização com Amostra de Imóveis Colorida por Tipo

Para identificar a distribuição e popularidade dos diferentes tipos de acomodação (quarto privado, apartamento inteiro, quarto compartilhado), selecionamos uma amostra de 100 imóveis e colorimos os pinos no mapa de acordo com o tipo de acomodação. Cada tipo é representado por uma cor distinta, o que facilita a análise da concentração de cada categoria nas regiões de Nova York.

- **Quarto Privado**: Cor verde escura
- **Apartamento Inteiro**: Cor vermelha escura
- **Quarto Compartilhado**: Cor roxa

```python
# Amostra de 100 imóveis e adição de uma coluna de cores para o tipo de quarto
amostra_imoveis = data[['neighbourhood_group', 'room_type', 'latitude', 'longitude']].sample(100)
amostra_imoveis['color'] = amostra_imoveis['room_type'].map({
    'Private room': 'darkgreen',
    'Entire home/apt': 'darkred',
    'Shared room': 'purple'
})

# Criar o mapa centrado na média das coordenadas da amostra
mapa_amostra = folium.Map(location=[amostra_imoveis['latitude'].mean(), amostra_imoveis['longitude'].mean()], zoom_start=12)

# Adicionar os pinos coloridos ao mapa
for _, row in amostra_imoveis.iterrows():
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=f"{row['neighbourhood_group']} - {row['room_type']}",
        icon=folium.Icon(color=row['color'])
    ).add_to(mapa_amostra)

# Exibir o mapa com amostra colorida por tipo de quarto
mapa_amostra
