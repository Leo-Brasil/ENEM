import streamlit as st

# Adicionando icone a aba
st.set_page_config(page_icon='enem icon.png')

# Definindo as páginas
main_page = st.Page('primeira pagina.py', title='Página Principal')
page2 = st.Page('segunda pagina.py', title='Análise Explorativa de Dados')
page3 = st.Page('terceira pagina.py', title='Página Oculta')

# Toggle: deixe True para ocultar page2 enquanto trabalha nela
HIDE_PAGE3 = True

# Ajustar Navegação (mantém a página no projeto, mas oculta da navegação)
pages = [main_page, page2]
if not HIDE_PAGE3:
    pages.append(page3)

pg = st.navigation(pages)

# Run the selected page
pg.run()