import requests
import streamlit as st

# Ajuste o endpoint conforme o ambiente (local ou em contêiner)
API_BASE_URL = "http://flask-app:5000/pipeline/"  # Ajuste para o ambiente correto

def get_similar_products_by(cod_loja, cod_prod):
    payload = {
        "cod_loja": cod_loja,
        "cod_prod": cod_prod
    }

    try:
        response = requests.post(f"{API_BASE_URL}get_similar_products", json=payload)

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            try:
                # Verifica se o conteúdo da resposta é JSON e se contém a chave 'data'
                result = response.json()

                if 'data' in result:
                    return result['data']
                else:
                    st.error("Erro: Resposta inesperada do servidor. 'data' não encontrado.")
                    return []
            except ValueError:
                st.error("Erro ao decodificar a resposta do servidor. Resposta não está em formato JSON.")
                return []
        else:
            st.error(f"Erro: {response.status_code} - {response.text}")
            return []

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao tentar se conectar ao servidor: {e}")
        return []
