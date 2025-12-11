import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import streamlit as st
import numpy as np
import plotly.express as px
import statsmodels as sm

# Chamar antes de qualquer st.* para usar largura total da página
st.set_page_config(page_title="Análise Exploratória dos Dados", layout="wide")

# Definir função para carga de dados
def carregar_dados(csv_name):
    df = pd.read_csv(csv_name, encoding="latin1", sep=";")
    return df

# Carrega e exibe os dados
df = carregar_dados('dados_reduzidos.csv')
st.title("Dados Reduzidos do ENEM 2023 - Alunos Presentes")
st.subheader('Prévia dos 100 primeiros resultados')
st.dataframe(df.head(100),hide_index=True)

# Mapa de cor
palette = {
    'Feminino': '#f28cb1',
    'Masculino': '#5dade2'
}

# Colunas para Gráficos
col_notas = [
    'Nota Ciências da Natureza',
    'Nota Ciências Humanas',
    'Nota Linguagens e Códigos',
    'Nota Matemática'
]

# Limpando os dados
df_limpo = df[(df[col_notas]>0).all(axis=1)]

cols = st.columns(2, gap="medium")

with cols[0]:
    st.subheader("Quantidade de Provas Realizadas por Federação")
    ordem = df_limpo['Sigla Federacao Prova'].value_counts().index.tolist()

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.countplot(data=df_limpo, y='Sigla Federacao Prova', palette=palette, hue='Sexo', order=ordem, ax=ax)

    ax.set_xlabel('Quantidade Inscritos')
    ax.set_ylabel('Locais Realizacao Provas')

    # Adiciona rótulos com os valores em cada barra
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', fontsize=8)

    st.pyplot(fig)

with cols[1]:
    st.subheader("Quantidade de Provas realizadas por Faixa Etaria")
    ordem_faixa_etaria = sorted(df_limpo['Faixa Etaria'].unique())
    if 'Menor de 17 anos' in ordem_faixa_etaria:
        ordem_faixa_etaria.remove('Menor de 17 anos')
        ordem_faixa_etaria.insert(0,'Menor de 17 anos')

    fig, contagem_estado = plt.subplots(figsize= (12.5,8))
    contagem_estado = sns.countplot(df_limpo,y='Faixa Etaria', palette=palette, hue = 'Sexo', order = ordem_faixa_etaria)

    contagem_estado.set_xlabel('Quantidade Inscritos')
    contagem_estado.set_ylabel('Faixa Etaria')

    for container in contagem_estado.containers:
        contagem_estado.bar_label(container, fmt = '%d', fontsize = 8)

    st.pyplot(fig)

st.subheader("Distribuição Percentual de Sexo (Gráfico de Rosca)")

counts = df_limpo['Sexo'].value_counts()
labels = counts.index
sizes = counts.values
colors = [palette[label] for label in labels]

# Montando gráfico de rosca
fig, ax = plt.subplots(figsize = (16,4))
ax.pie(
    sizes,
    labels = labels,
    autopct = '%1.1f%%',
    startangle = 90,
    colors = colors,
    wedgeprops = dict(width = 0.2)
)
ax.axis('equal')
st.pyplot(fig)

st.subheader('Análise Distribuição Notas Matemática')

# Função para auxiliar nos cálculos e exibir em uma coluna especifica
def display_stats(column, data_series, name):
    media = np.mean(data_series)
    minimo = np.min(data_series)
    maximo = np.max(data_series)
    q1 = np.quantile(data_series, 0.25)
    q2 = np.quantile(data_series, 0.5)
    q3 = np.quantile(data_series, 0.75)
    interquartil = q3 - q1
    limite_inferior = q1 - (1.5 * interquartil)
    limite_superior = q3 + (1.5 * interquartil)
    quantidade_outlier_abaixo = len(data_series[data_series < limite_inferior])
    quantidade_outlier_acima = len(data_series[data_series > limite_superior])
                                   
    with column:
        st.write('')
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >{name}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Média: {media: 2f}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Mínimo: {minimo: 2f}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Máximo: {maximo: 2f}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Q1: {q1: 2f}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Q2: {q2: 2f}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Q3: {q3: 2f}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Interquartil: {interquartil: 2f}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Limite Inferior{limite_inferior: 2f}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Limite Superior: {limite_superior: 2f}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Outlier Abaixo L.I.: {quantidade_outlier_abaixo: 2f}</span>", unsafe_allow_html=True)
        st.write(f"<span style='font-size: 12px; font-weight: bold;' >Outlier Acima L.S.:{quantidade_outlier_acima: 2f}</span>", unsafe_allow_html=True)

# Criar duas colunas
col1,col2, col3, col4 = st.columns(4)
column_map = {
    'Nota Ciências da Natureza': col1,
    'Nota Ciências Humanas': col2,
    'Nota Linguagens e Códigos': col3,
    'Nota Matemática': col4
}
# Itera sobre os nomes das colunas e chama a função para exbir em sua respectiva coluna no layout
for name in col_notas:
    target_column = column_map[name]
    display_stats(target_column, df_limpo[name], name)

st.divider()

df_limpo_long = df_limpo.melt(
    id_vars = ['Numero Inscricao'],
    value_vars = col_notas,
    var_name = 'Materia',
    value_name = 'Nota'
)

fig = px.box(df_limpo_long, x = 'Materia', y = 'Nota', color = 'Materia', notched = True)
st.plotly_chart(fig,use_container_width=False)

st.subheader('Distribuição Normal')

cols = st.columns(2, gap = 'small')
with cols [0]: 
    fig_hist = px.histogram(
        df_limpo,
        x='Nota Ciências da Natureza',
        nbins = 50,
        title = 'Distribuição das Notas Ciências da Natureza',
        marginal = 'box',
        color_discrete_sequence = ['green']
    )
    st.plotly_chart(fig_hist,use_container_width=True)
    # Outro Gráfico nas mesma coluna
    fig_hist = px.histogram(
        df_limpo,
        x='Nota Ciências Humanas',
        nbins = 50,
        title = 'Distribuição das Notas Ciências Humanas',
        marginal = 'box',
        color_discrete_sequence = ['green']
    )
    st.plotly_chart(fig_hist,use_container_width=True)

with cols [1]: 
    fig_hist = px.histogram(
        df_limpo,
        x='Nota Linguagens e Códigos',
        nbins = 50,
        title = 'Distribuição das Notas Linguagens e Códigos',
        marginal = 'box',
        color_discrete_sequence = ['green']
    )
    st.plotly_chart(fig_hist,use_container_width=True)
    # Outro Gráfico nas mesma coluna
    fig_hist = px.histogram(
        df_limpo,
        x='Nota Matemática',
        nbins = 50,
        title = 'Distribuição das Notas Matemática',
        marginal = 'box',
        color_discrete_sequence = ['green']
    )
    st.plotly_chart(fig_hist,use_container_width=True)

st.subheader('Correlação: Linguagens e Código x Matemática')
#Criando uma amostragem
df_limpo_amostragem = df_limpo.sample(n=5000, random_state=42)

# Criando Gráfico
df_scatter = df_limpo_amostragem.dropna(subset = ['Nota Linguagens e Códigos', 'Nota Matemática'])
fig = px.scatter(
    df_scatter,
    x = 'Nota Linguagens e Códigos',
    y = 'Nota Matemática',
    opacity = 0.5,
    labels = {
        'Nota Linguagens e Códigos': 'Nota em Linguagens',
        'Nota Matemática': 'Nota em  Matemática' 
    },
    trendline = 'ols'
)
st.plotly_chart(fig,use_container_width=True)