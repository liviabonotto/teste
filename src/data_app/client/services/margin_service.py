import requests
import pandas as pd
import streamlit as st

API_BASE_URL = "http://flask-app:5000/margin/"

def get_similar_product_by_margin(descricao, categoria, sub_categoria, marca, preco_max, preco_min):
    payload = {
        "descricao": descricao,
        "categoria": categoria,
        "subcategoria": sub_categoria,
        "marca": marca,
        "preco_max": preco_max,
        "preco_min": preco_min
    }
    
    response = requests.post(f"{API_BASE_URL}get_similar_product_by_margin_bronze", json=payload)
    
    if response.status_code == 200:
        produtos_similares = response.json()
        return produtos_similares
    else:
        st.error(f"Erro: {response.json().get('error', 'Erro desconhecido')}")
        return []
    
def get_product_categories():
    response = requests.get(f"{API_BASE_URL}get_product_categories")
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro ao buscar categorias: {response.json().get('error', 'Erro desconhecido')}")
        return []

def get_product_subcategories():
    response = requests.get(f"{API_BASE_URL}get_product_subcategories")
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro ao buscar subcategorias: {response.json().get('error', 'Erro desconhecido')}")
        return []

def get_product_brands():
    response = requests.get(f"{API_BASE_URL}get_product_brands")
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro ao buscar marcas: {response.json().get('error', 'Erro desconhecido')}")
        return []