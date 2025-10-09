import streamlit as st
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_avatar import avatar
from streamlit_card import card
from streamlit_extras.chart_annotations import get_annotations_chart
from streamlit_extras.chart_container import chart_container
import altair as alt
import numpy as np
from streamlit_extras.concurrency_limiter import concurrency_limiter
import time
from streamlit_extras.customize_running import center_running
from streamlit_faker import get_streamlit_faker
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stodo import to_do
from streamlit_extras.stoggle import stoggle
from streamlit_extras.echo_expander import echo_expander


# Deixando as informações mais distribuidas
st.set_page_config(layout="wide")

# Adicionado imagem a segunda pagina
with st.sidebar:
    st.image('laboratorio.png', width=200)

# Função carregar estilo externo
def carregarestilo(caminho):
    with open(caminho) as f:
        st.markdown(f"<style>{f.read()}</style",unsafe_allow_html=True)

# Aplicando o CSS
carregarestilo('estilo.css')

def example():
    avatar(
        [
            {
                "url": "https://picsum.photos/id/237/300/300",
                "size": 40,
                "title": "Sam",
                "caption": "hello",
                "key": "avatar1",
            },
            {
                "url": "https://picsum.photos/id/238/300/300",
                "size": 40,
                "title": "Bob",
                "caption": "happy",
                "key": "avatar2",
            },
            {
                "url": "https://picsum.photos/id/23/300/300",
                "size": 40,
                "title": "Rick",
                "caption": "Bye",
                "key": "avatar3",
            },
        ]
    )
example()

def example2():
    card(
        title="Hello World!",
        text="Some description",
        image="http://placekitten.com/300/250",
        url="https://www.google.com",
    )

example2()

def get_data() -> pd.DataFrame:
    # Exemplo de dados fictícios
    return pd.DataFrame({
        'date': pd.date_range(start='2007-01-01', periods=100, freq='M'),
        'GOOG': pd.Series(range(100)) + 500,
        'AAPL': pd.Series(range(100)) + 300,
    })

def get_chart(data: pd.DataFrame) -> alt.Chart:
    base = alt.Chart(data).transform_fold(
        ['GOOG', 'AAPL'],
        as_=['Company', 'Price']
    ).mark_line().encode(
        x='date:T',
        y='Price:Q',
        color='Company:N'
    )
    return base

def get_annotations_chart(annotations):
    annotations_df = pd.DataFrame(annotations, columns=['date', 'note'])
    annotations_df['date'] = pd.to_datetime(annotations_df['date'])

    return alt.Chart(annotations_df).mark_text(
        align='left', baseline='middle', dx=5
    ).encode(
        x='date:T',
        y=alt.value(500),
        text='note'
    )

def example3() -> None:
    data = get_data()
    chart = get_chart(data=data)

    chart += get_annotations_chart([
        ("2008-03-01", "Pretty good day for GOOG"),
        ("2007-12-01", "Something's going wrong for GOOG & AAPL"),
        ("2008-11-01", "Market starts again thanks to..."),
        ("2009-12-01", "Small crash for GOOG after..."),
    ])

    st.altair_chart(chart, use_container_width=True)

example3()

def get_random_data():
    return pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )

def chart_container(data):
    return st.container()

def example4():
    chart_data = get_random_data()
    with chart_container(chart_data):
        st.write("Here's a cool chart")
        st.area_chart(chart_data)

example4()

def example5():
    @concurrency_limiter(max_concurrency=1)
    def heavy_computation():
        st.write("Heavy computation")
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.15)
            my_bar.progress(percent_complete + 1, text=progress_text)
        st.write("END OF Heavy computation")
        return 42

    my_button = st.button("Run heavy computation")

    if my_button:
        heavy_computation()

example5()

def example6():
    click = st.button("Observe where the 🏃‍♂️ running widget is now!")
    if click:
        center_running()
        time.sleep(2)

example6()

def example7():
    fake = get_streamlit_faker(seed=42)
    fake.markdown()
    fake.info(icon="💡", body="You can also pass explicit parameters!")
    fake.selectbox()
    fake.slider()
    fake.metric()
    fake.altair_chart()
    
example7()

def example8():
    col1, col2, col3 = st.columns(3)

    col1.metric(label="Gain", value=5000, delta=1000)
    col2.metric(label="Loss", value=5000, delta=-1000)
    col3.metric(label="No Change", value=5000, delta=0)

    style_metric_cards()
example8()

def example9():
    to_do(
        [(st.write, "☕ Take my coffee")],
        "coffee",
    )
    to_do(
        [(st.write, "🥞 Have a nice breakfast")],
        "pancakes",
    )
    to_do(
        [(st.write, ":train: Go to work!")],
        "work",
    )
example9()

def example10():
    stoggle(
        "Click me!",
        """🥷 Surprise! Here's some additional content""",
    )
example10()


cols = st.columns(3, gap="medium")
with cols[0]:
    avatar(
        [
            {
                "url": "https://picsum.photos/id/237/300/300",
                "size": 40,
                "title": "Sam",
                "caption": "hello",
                "key": "avatar1",
            }
        ]
    )
with cols[1]:
    avatar(
        [
            {
                "url": "https://picsum.photos/id/238/300/300",
                "size": 40,
                "title": "Bob",
                "caption": "happy",
                "key": "avatar2",
            }
        ]
    )
with cols[2]:
    avatar(
        [
            {
                "url": "https://picsum.photos/id/23/300/300",
                "size": 40,
                "title": "Rick",
                "caption": "Bye",
                "key": "avatar3",
            }
        ]
    )

with echo_expander(): #Serve apenas para codigo
    st.write('Teste de Quadro Expandido e codigo')

with st.expander('teste'):#Serve para anotação
    st.write('teste')

df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)

st.dataframe(df, use_container_width=True)