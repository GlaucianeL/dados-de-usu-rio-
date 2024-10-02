#ALUNA : Glauciane Lages da Silva

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import folium
from streamlit_folium import folium_static

st.title('DADOS DE TRANSPORTE : Atendimento ao Usuário - Concessionárias')  # Título da página
st.header("Glauciane Lages da Silva :sunglasses:")
st.header( "Dados da Agência Nacional de Transportes Terrestres - ANTT")
st.write("A Agência Nacional de Transportes Terrestres é uma autarquia sob regime especial que tem por finalidade regular, supervisionar e fiscalizar as atividades de prestação de serviços e de exploração da infraestrutura de transportes, exercidas por terceiros, visando garantir a movimentação de pessoas e bens, harmonizar os interesses dos usuários com os das empresas concessionárias, permissionárias, autorizadas e arrendatárias, e de entidades delegadas, preservado o interesse público, arbitrar conflitos de interesses e impedir situações que configurem competição imperfeita ou infração contra a ordem econômica.")
st.header("Processos Produtivos Inteligentes", divider=True)

# URL do JSON
url = "https://dados.antt.gov.br/dataset/6bb7a82d-72ef-427f-92b3-4e490a3896ca/resource/2c94bcd0-b8f1-49d0-aa30-7988feab4d9d/download/atendimento_usuario.json"

# Obter os dados
response = requests.get(url)
data = response.json()
st.image("com.webp", caption="atendimento ao usuario")
# Converter para DataFrame
df = pd.DataFrame(data['atendimento_usuario'])
df['Total_do_Atendimento'] = df['Total_do_Atendimento'].astype(int)

# Para o exemplo, adicionando coordenadas fictícias
# Substitua por dados reais se disponíveis
coordenadas = {
    "AUTOPISTA FERNÃO DIAS": (-23.7045, -46.6728)  # Exemplo de coordenadas
}

# Adicionar colunas de latitude e longitude
df['Latitude'] = df['Concessionaria'].map(lambda x: coordenadas.get(x, (None, None))[0])
df['Longitude'] = df['Concessionaria'].map(lambda x: coordenadas.get(x, (None, None))[1])

# Título da aplicação
st.title("Análise de Atendimento ao Usuário")

# Mostrar a tabela
st.subheader("Tabela de Dados")
st.dataframe(df)

# Gráfico de total de atendimentos por tipo
st.subheader("Total de Atendimentos por Mês e Tipo")
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='Mes_Ano', y='Total_do_Atendimento', hue='Tipo_de_atendimento')
plt.title('Total de Atendimentos por Mês e Tipo')
plt.xticks(rotation=45)
plt.xlabel('Mês/Ano')
plt.ylabel('Total de Atendimentos')
plt.legend(title='Tipo de Atendimento')
st.pyplot(plt)

# Gráfico de linha para visualização de tendência
st.subheader("Tendência de Atendimentos por Tipo ao Longo do Tempo")
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Mes_Ano', y='Total_do_Atendimento', hue='Tipo_de_atendimento', marker='o')
plt.title('Tendência de Atendimentos por Tipo ao Longo do Tempo')
plt.xticks(rotation=45)
plt.xlabel('Mês/Ano')
plt.ylabel('Total de Atendimentos')
plt.legend(title='Tipo de Atendimento')
st.pyplot(plt)


# Gráfico de pizza para proporção de tipos de atendimento
st.subheader("Proporção de Tipos de Atendimento")
tipo_atendimentos = df.groupby('Tipo_de_atendimento')['Total_do_Atendimento'].sum()
plt.figure(figsize=(8, 8))
plt.pie(tipo_atendimentos, labels=tipo_atendimentos.index, autopct='%1.1f%%', startangle=140)
plt.title('Proporção de Tipos de Atendimento')
st.pyplot(plt)

# Mapa das concessionárias
st.subheader("Mapa das Concessionárias")
mapa = folium.Map(location=[-23.7045, -46.6728], zoom_start=6)  # Centraliza o mapa em um ponto

for _, row in df.iterrows():
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Concessionaria']}: {row['Total_do_Atendimento']}",
            icon=folium.Icon(color="blue"),
        ).add_to(mapa)

folium_static(mapa)