import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import streamlit as st

def carregar_dados(csv_name):
    df = pd.read_csv(csv_name, encoding="latin1", sep=";")
    return df

# Carrega e exibe os dados
df = carregar_dados('dados_reduzidos.csv')
st.title("Dados Reduzidos do ENEM 2023 - Alunos Presentes")
st.header('Prévia dos 50 primeiros resultados')
st.dataframe(df.head(50))