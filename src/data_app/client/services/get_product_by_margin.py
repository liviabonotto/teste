import requests
import pandas as pd
import streamlit as st

API_URL = "http://flask-app:5000/pipeline/get_similar_product_by_margin"

def get_similar_product_by_margin(descricao):
    response = requests.post(API_URL, json={"descricao": descricao})
    
    if response.status_code == 200:
        produtos_similares = response.json()
        return pd.DataFrame(produtos_similares) 
    else:
        st.error(f"Erro: {response.json().get('error', 'Erro desconhecido')}")