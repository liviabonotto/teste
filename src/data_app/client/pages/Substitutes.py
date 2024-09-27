import streamlit as st
from services.subs_service import get_substitute_products

# Custom CSS for formatting
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    div.product-card {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        background-color: #262730;
    }
    h4.product-name {
        font-weight: bold;
    }
    p.product-price, p.product-margin {
        color: #32B950;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Page Title
st.title("Sugestão de produtos")
st.write("Informe o ID de um produto e de uma loja para receber sugestões de produtos substitutos.")

# Input Form with empty default values
col1, col2 = st.columns(2)
with col1:
    cod_prod = st.text_input("ID do produto", value="")
with col2:
    cod_loja = st.text_input("ID da loja", value="")

# Button to Submit
search = st.button("Enviar")

# Process inputs and show results
if search:
    if cod_prod and cod_loja:
        substitutos = get_substitute_products(cod_prod, cod_loja)

        # Handle API response errors or invalid responses
        if isinstance(substitutos, str):
            st.error(substitutos)
        elif isinstance(substitutos, list):
            # Ensure each item in the list is a dictionary before sorting
            if all(isinstance(item, dict) for item in substitutos):
                
                # Sorting options
                order_by = st.selectbox("Ordenar por", ["Margem de lucro", "Preço"])

                if order_by == "Margem de lucro":
                    substitutos = sorted(substitutos, key=lambda x: x.get("margem", 0), reverse=True)
                elif order_by == "Preço":
                    substitutos = sorted(substitutos, key=lambda x: x.get("preco", 0), reverse=True)

                # Display each product
                for product in substitutos:
                    st.markdown(f"""
                    <div class="product-card">
                        <h4 class="product-name">{product.get('nome', 'Sem nome')} - {product.get('id', 'Sem ID')}</h4>
                        <p>{product.get('descricao', 'Sem descrição')}</p>
                        <p>Preço: <span class="product-price">R$ {product.get('preco', 0):.2f}</span></p>
                        <p>Margem: <span class="product-margin">{product.get('margem', 'Sem margem')}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Os dados retornados não estão no formato correto.")
        else:
            st.write("Nenhum produto substituto encontrado.")
    else:
        st.error("Por favor, preencha tanto o ID do produto quanto o ID da loja.")
