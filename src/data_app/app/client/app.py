import streamlit as st
import pandas as pd
from utils.database import fetch_price_data

st.title("Price View Dashboard")

df = fetch_price_data()

st.sidebar.header("Filtros")

cod_prod_list = df['cod_prod'].unique()
cod_prod_selected = st.sidebar.multiselect("Selecione o Código do Produto", cod_prod_list, default=cod_prod_list)

if not df['preco'].empty and df['preco'].min() != df['preco'].max():
    preco_min, preco_max = st.sidebar.slider(
        "Selecione o Intervalo de Preço",
        int(df['preco'].min()),
        int(df['preco'].max()),
        (int(df['preco'].min()), int(df['preco'].max()))
    )
    df_filtered = df[(df['cod_prod'].isin(cod_prod_selected)) & (df['preco'] >= preco_min) & (df['preco'] <= preco_max)]
else:
    st.sidebar.write("Não há variação nos preços disponíveis para filtrar.")
    df_filtered = df[df['cod_prod'].isin(cod_prod_selected)]

st.dataframe(df_filtered)

st.subheader("Evolução de Preços ao Longo do Tempo")
if not df_filtered.empty:
    st.line_chart(df_filtered[['data_inicio_preco', 'preco']].set_index('data_inicio_preco'))
else:
    st.write("Nenhum dado disponível para exibir o gráfico.")

st.subheader("Estatísticas Descritivas")
if not df_filtered.empty:
    st.write(df_filtered.describe())
else:
    st.write("Nenhum dado disponível para exibir as estatísticas.")