import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DASHFLIX — Análise do Catálogo",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #374151;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/filmes_netflix.csv")
    df['director'] = df['director'].fillna('Not Given')
    df['country'] = df['country'].fillna('Not Given')
    return df

df = load_data()

st.title("DASHFLIX — Dashboard do Catálogo de Filmes")
st.caption("Análise Estratégica de Dados e Portfólio de Streaming | Framework C.I.A.")
st.markdown("---")

st.sidebar.header("Filtros do Catálogo")

ano_min = int(df['release_year'].min())
ano_max = int(df['release_year'].max())
anos_selecionados = st.sidebar.slider(
    "Ano de Lançamento:",
    min_value=ano_min,
    max_value=ano_max,
    value=(2000, ano_max)
)

df_filtered = df[
    (df['release_year'] >= anos_selecionados[0]) & 
    (df['release_year'] <= anos_selecionados[1])
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Filmes", f"{len(df_filtered):,}")
col2.metric("Duração Média", f"{df_filtered['duracao_min'].mean():.1f} min")
col3.metric("Mediana de Duração", f"{df_filtered['duracao_min'].median():.0f} min")
col4.metric("Anos de Abrangência", f"{anos_selecionados[0]} - {anos_selecionados[1]}")

st.markdown("---")

genres_list = []
for genres in df_filtered['listed_in'].dropna():
    genres_list.extend([g.strip() for g in genres.split(',')])

df_genres = pd.Series(genres_list).value_counts().reset_index()
df_genres.columns = ['Gênero', 'Quantidade']

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 Gêneros Mais Frequentes")
    fig_genres = px.bar(
        df_genres.head(10),
        x='Quantidade',
        y='Gênero',
        orientation='h',
        color='Quantidade',
        color_continuous_scale='Reds',
        text='Quantidade'
    )
    fig_genres.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_genres, use_container_width=True)

with col_right:
    st.subheader("Distribuição por Classificação Indicativa")
    rating_counts = df_filtered['rating'].value_counts().head(6).reset_index()
    rating_counts.columns = ['Rating', 'Quantidade']
    
    fig_rating = px.pie(
        rating_counts,
        names='Rating',
        values='Quantidade',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_rating.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_rating, use_container_width=True)

st.markdown("---")
st.subheader("Detalhamento do Acervo de Filmes")
st.dataframe(
    df_filtered[['title', 'director', 'country', 'release_year', 'rating', 'duracao_min', 'listed_in']],
    use_container_width=True
)