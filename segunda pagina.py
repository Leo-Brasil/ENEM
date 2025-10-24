import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import streamlit as st

# Chamar antes de qualquer st.* para usar largura total da página
st.set_page_config(page_title="Análise Exploratória dos Dados", layout="wide")

def carregar_dados(csv_name):
    df = pd.read_csv(csv_name, encoding="latin1", sep=";")
    return df

# Carrega e exibe os dados
df = carregar_dados('dados_reduzidos.csv')
st.title("Dados Reduzidos do ENEM 2023 - Alunos Presentes")
st.subheader('Prévia dos 50 primeiros resultados')
st.dataframe(df.head(50))

cols = st.columns(2, gap="medium")

with cols[0]:
    st.subheader("Quantidade de Provas Realizadas por Federação")
    ordem = df['Sigla Federacao Prova'].value_counts().index.tolist()

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.countplot(data=df, y='Sigla Federacao Prova', palette='pastel', hue='Sexo', order=ordem, ax=ax)

    ax.set_xlabel('Quantidade Inscritos')
    ax.set_ylabel('Locais Realizacao Provas')

    # Adiciona rótulos com os valores em cada barra
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', fontsize=8)

    st.pyplot(fig)

with cols[1]:
    st.subheader("Quantidade de Provas realizadas por Faixa Etaria")
    ordem_faixa_etaria = sorted(df['Faixa Etaria'].unique())
    if 'Menor de 17 anos' in ordem_faixa_etaria:
        ordem_faixa_etaria.remove('Menor de 17 anos')
        ordem_faixa_etaria.insert(0,'Menor de 17 anos')

    fig, contagem_estado = plt.subplots(figsize= (12.5,8))
    contagem_estado = sns.countplot(df,y='Faixa Etaria', palette='pastel', hue = 'Sexo', order = ordem_faixa_etaria)

    contagem_estado.set_xlabel('Quantidade Inscritos')
    contagem_estado.set_ylabel('Faixa Etaria')

    for container in contagem_estado.containers:
        contagem_estado.bar_label(container, fmt = '%d', fontsize = 8)

    st.pyplot(fig)