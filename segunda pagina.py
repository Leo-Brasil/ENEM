import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import streamlit as st
import zipfile

# Caminho do ZIP e nome do CSV dentro dele
zip_path = "dados_reduzidos.zip"
csv_name = "dados_reduzidos.csv"

@st.cache_data
def carregar_dados_zip(zip_path, csv_name):
    # Extrai o CSV se ainda não estiver extraído
    if not os.path.exists(csv_name):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extract(csv_name)

    # Carrega o CSV
    df = pd.read_csv(csv_name, encoding="latin1", sep=";")
    return df

# Carrega e exibe os dados
df = carregar_dados_zip(zip_path, csv_name)
st.title("Dados Reduzidos do ENEM 2023")
st.dataframe(df.head(50))  # Mostra os primeiros 50 registros