import requests
import streamlit as st

API_BASE_URL = "http://flask-app:5000/"  # Adjust this as needed

def get_substitute_products(cod_prod, cod_loja):
    payload = {
        "cod_prod": cod_prod,
        "cod_loja": cod_loja
    }

    try:
        response = requests.post(f"{API_BASE_URL}get_product_substitute", json=payload)

        # Check if response content is valid JSON
        if response.status_code == 200:
            try:
                result = response.json()  # Attempt to parse JSON
                # Add debugging print statements to see what response is coming from the API
                print(f"API Response: {result}")
                return result
            except ValueError:
                st.error("Erro ao decodificar a resposta do servidor. Resposta não está em formato JSON.")
                return []
        else:
            st.error(f"Erro: {response.status_code} - {response.text}")
            return []

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao tentar se conectar ao servidor: {e}")
        return []
