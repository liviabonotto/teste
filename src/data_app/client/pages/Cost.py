import streamlit as st
import pandas as pd
from services.view_service import fetch_data

st.title("Cost View Dashboard")

cost_data = fetch_data("cost")
st.write(cost_data)

st.sidebar.header("Filtros")

if not cost_data['custo'].empty and cost_data['custo'].min() != cost_data['custo'].max():
    cost_min, cost_max = st.sidebar.slider(
        "Selecione o Intervalo de Custo",
        int(cost_data['custo'].min()),
        int(cost_data['custo'].max()),
        (int(cost_data['custo'].min()), int(cost_data['custo'].max()))
    )
    df_filtered = cost_data[(cost_data['custo'] >= cost_min) & (cost_data['custo'] <= cost_max)]
else:
    st.sidebar.write("Não há variação nos custos disponíveis para filtrar.")
    df_filtered = cost_data

st.dataframe(df_filtered)

st.subheader("Evolução de Custos ao Longo do Tempo")
if not df_filtered.empty:
    st.line_chart(df_filtered[['data_inicio_custo', 'custo']].set_index('data_inicio_custo'))
else:
    st.write("Nenhum dado disponível para exibir o gráfico.")

st.subheader("Estatísticas Descritivas")
if not df_filtered.empty:
    st.write(df_filtered.describe())
else:
    st.write("Nenhum dado disponível para exibir as estatísticas.")
