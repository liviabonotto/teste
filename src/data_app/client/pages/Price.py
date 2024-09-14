import streamlit as st
import pandas as pd
from services.view_service import fetch_data

st.title("Price View Dashboard")

price_data = fetch_data("price")

st.sidebar.header("Filtros")

if not price_data['preco'].empty and price_data['preco'].min() != price_data['preco'].max():
    price_min, price_max = st.sidebar.slider(
        "Selecione o Intervalo de Preço",
        int(price_data['preco'].min()),
        int(price_data['preco'].max()),
        (int(price_data['preco'].min()), int(price_data['preco'].max()))
    )
    df_filtered = price_data[(price_data['preco'] >= price_min) & (price_data['preco'] <= price_max)]
else:
    st.sidebar.write("Não há variação nos preços disponíveis para filtrar.")
    df_filtered = price_data

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
