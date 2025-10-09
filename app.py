import streamlit as st

# Adicionando icone a aba
st.set_page_config(page_icon='enem icon.png')

# Definindo as páginas
main_page = st.Page('primeira pagina.py', title= 'Página Principal')
page2 = st.Page('segunda pagina.py', title = 'Teste Funcionalidade')

# Ajustar Navegação
pg = st.navigation([main_page,page2])

# Run the selected page
pg.run()