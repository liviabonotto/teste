import requests
import streamlit as st

API_BASE_URL = "http://flask-app:5000/"  # Ajuste para o ambiente correto

def get_substitute_products(cod_prod, cod_loja):
    payload = {
        "cod_prod": cod_prod,
        "cod_loja": cod_loja
    }

    try:
        #st.write("Payload enviado:", payload)  # Log do payload enviado

        response = requests.post(f"{API_BASE_URL}get_product_substitute", json=payload)

        # Check if response content is valid JSON
        if response.status_code == 200:
            try:
                result = response.json()  # Attempt to parse JSON
                
                #st.write("Resposta recebida:", result)  # Log da resposta recebida

                # Check if the response contains an error
                if 'error' in result:
                    st.error(result['error'])
                    return []
                
                # Ensure the result is a list of dictionaries
                if isinstance(result, list):
                    for product in result:
                        if isinstance(product, dict):
                            # Mocking the price and margin fields
                            product['preco'] = 50.00  # Mocked price
                            product['margem'] = "25%"  # Mocked margin
                        else:
                            st.error(f"Unexpected product format: {product}")
                            return []
                
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
