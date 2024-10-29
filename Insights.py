import pandas as pd
import numpy as np
import plotly.express as px
import folium
from matplotlib import pyplot as plt

# Carregar dados
data = pd.read_csv('/content/AB_NYC_2019.csv')

# Exibir as primeiras linhas do conjunto de dados
data.head()

# Análise exploratória dos preços
# Calcular o valor médio do preço
valor_medio = np.mean(data['price'])
print(f'O valor médio é: U$ {valor_medio:.2f}')
# Resposta esperada: U$ 152.72

# Identificar regiões únicas
regioes_unicas = pd.unique(data['neighbourhood_group'])
print('Regiões únicas:', regioes_unicas)
# Resposta esperada: 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx'

# Encontrar o valor máximo do preço
preco_maximo = np.max(data['price'])
print(f'Preço máximo: U$ {preco_maximo}')
# Resposta esperada: U$ 10.000

# Análise dos tipos de quarto
room_type_unique = np.unique(data['room_type'])
print('Categorias de tipos de quarto:', room_type_unique)
# Resposta esperada: 'Entire home/apt', 'Private room', 'Shared room'

# Identificar anfitriões únicos
host_id_unique = np.unique(data['host_id'])
print(f'Número de anfitriões únicos: {len(host_id_unique)}')
# Resposta esperada: 37.457 hosts únicos

# Calcular o desvio padrão dos preços
desvio_padrao = np.std(data['price'])
print(f'Desvio padrão dos preços: U$ {desvio_padrao:.2f}')
# Resposta esperada: U$ 240.15

# Filtrar preços abaixo de 1250 e criar histograma
filtered_price = data[data['price'] < 1250]['price']
plt.hist(filtered_price, bins=12)
plt.title("Distribuição de preços (até U$ 1250)")
plt.xlabel("Preço")
plt.ylabel("Frequência")
plt.show()
# Resposta: Existem mais de 20.000 imóveis com valor de aluguel até U$ 100,00

# Filtrar imóveis com menos de 300 avaliações e criar histograma
filtered_reviews = data[data['number_of_reviews'] < 300]['number_of_reviews']
plt.hist(filtered_reviews, bins=12)
plt.title("Distribuição do número de avaliações (até 300)")
plt.xlabel("Número de Avaliações")
plt.ylabel("Frequência")
plt.show()
# Resposta: Existem quase 30.000 imóveis com até 10 avaliações.

# Análise de preço por região - Gráfico de Barras
data_grouped = data.groupby('neighbourhood_group')['price'].max().reset_index()
px.bar(data_grouped, x='neighbourhood_group', y='price', title='Preço Máximo por Região')

# Mapeamento dos imóveis por região
data_grouped = data.groupby('neighbourhood_group')[['latitude', 'longitude', 'price']].max().reset_index()
mapa = folium.Map(location=[data_grouped['latitude'].mean(), data_grouped['longitude'].mean()], zoom_start=12)

for _, row in data_grouped.iterrows():
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=f"{row['neighbourhood_group']} - Preço Máximo: U${row['price']}",
        icon=folium.Icon(color='blue')
    ).add_to(mapa)

# Exibir o mapa
mapa

# Amostra aleatória de imóveis e visualização com cores por tipo de quarto
amostra_imoveis = data[['neighbourhood_group', 'room_type', 'latitude', 'longitude']].sample(100)
amostra_imoveis['color'] = amostra_imoveis['room_type'].map({
    'Private room': 'darkgreen',
    'Entire home/apt': 'darkred',
    'Shared room': 'purple'
})

mapa_amostra = folium.Map(location=[amostra_imoveis['latitude'].mean(), amostra_imoveis['longitude'].mean()], zoom_start=12)

for _, row in amostra_imoveis.iterrows():
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=f"{row['neighbourhood_group']} - {row['room_type']}",
        icon=folium.Icon(color=row['color'])
    ).add_to(mapa_amostra)

# Exibir o mapa com amostra colorida por tipo de quarto
mapa_amostra
