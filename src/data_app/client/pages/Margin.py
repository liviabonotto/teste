import pandas as pd
import plotly.express as px
import streamlit as st
from services.get_product_by_margin import get_similar_product_by_margin
from services.view_service import fetch_data

st.set_page_config(page_title="Product Margin Dashboard", layout="wide")
st.title("Análise de Margens de Lucro")

df = fetch_data("margin")

descricao = st.text_input("Digite a descrição do produto:")

if st.button("Buscar Produto"):
    if descricao:
        df_resultado = get_similar_product_by_margin(descricao)
        
        if df_resultado is not None:
            st.subheader("Produtos Similares")
            st.dataframe(df_resultado)
        else:
            st.warning("Nenhum produto encontrado.")
    else:
        st.warning("Por favor, insira uma descrição.")

st.header("Margem de Lucro por Categoria")
categoria_margin = df.groupby('skd.categoria')['margem_lucro_bruto'].mean().reset_index()
fig_categoria = px.bar(categoria_margin, x='skd.categoria', y='margem_lucro_bruto', title='Margem de Lucro Média por Categoria')
st.plotly_chart(fig_categoria, use_container_width=True)

st.header("Margem de Lucro por Subcategoria")
subcategoria_margin = df.groupby('skd.sub_categoria')['margem_lucro_bruto'].mean().reset_index()
fig_subcategoria = px.bar(subcategoria_margin, x='skd.sub_categoria', y='margem_lucro_bruto', title='Margem de Lucro Média por Subcategoria')
st.plotly_chart(fig_subcategoria, use_container_width=True)