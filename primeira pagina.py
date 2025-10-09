import streamlit as st
import pandas as pd
from buscaAPI import process_years
from buscaAPI import exportar
from streamlit_extras.pdf_viewer import pdf_viewer

cols = st.columns(3,gap='medium')
with cols[0]:
    st.title("POC ENEM")
    st.write(f'Esse é uma POC para o ENEM utilizando o Streamlit.')
with cols[2]:
    st.image('enem icon.png')

# Deixando as informações mais distribuidas
st.set_page_config(layout="wide")

# Função carregar estilo externo
def carregarestilo(caminho):
    with open(caminho) as f:
        st.markdown(f"<style>{f.read()}</style",unsafe_allow_html=True)

# Inicializa o estado da checkbox
if "mostrar_resultado" not in st.session_state:
    st.session_state.mostrar_resultado = False

# Função para resetar a checkbox
def resetar_checkbox():
    st.session_state.mostrar_resultado = False

# Aplicando o CSS
carregarestilo('estilo.css')

# Carregando Log
with st.sidebar:
    st.image('enem.png',width=180)
    ano = st.sidebar.selectbox(
        'Qual ano você gostaria de receber o JSON do ENEM? (dados de 2015 até 2023)',
        list(range(2015,2024)),
        index = 0,
        key = 'ano',
        on_change = resetar_checkbox
    )

    formato = st.sidebar.selectbox(
        'Gostaria de ver o resultado em JSON ou DataFrame?',
        ['JSON','DataFrame'],
        index = 1,
        key='formato',
        on_change = resetar_checkbox
    )

st.checkbox('Mostrar resultado', key='mostrar_resultado')

# Executa a função se marcado
if st.session_state.mostrar_resultado:
    process_years(st.session_state.ano, st.session_state.formato)
    if st.button('Exportar resultado'):
        exportar(st.session_state.ano, st.session_state.formato)