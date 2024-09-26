import streamlit as st
from services.subs_service import get_substitute_products

# Custom CSS for button
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Page Title
st.title("Sugestão de produtos")
st.write("Informe o ID de um produto da compra para receber sugestão de um produto a ser vendido em conjunto, ou de um produto substituto.")

# Input Form with empty default values
col1, col2 = st.columns(2)
with col1:
    cod_prod = st.text_input("ID do produto", value="")
with col2:
    cod_loja = st.text_input("ID da loja", value="")

# Button to Submit
search = st.button("Enviar")

# Validate inputs and process when the button is clicked
if search:
    if cod_prod and cod_loja:
        substitutos = get_substitute_products(cod_prod, cod_loja)

        # Error handling for invalid product search
        if isinstance(substitutos, str):
            st.error(substitutos)
        elif substitutos:
            # Show product info and sort options
            order_by = st.selectbox("Ordenar por", ["Margem de lucro", "Preço"])
            
            if order_by == "Margem de lucro":
                substitutos = sorted(substitutos, key=lambda x: x["margem_lucro_bruto"], reverse=True)
            elif order_by == "Preço":
                substitutos = sorted(substitutos, key=lambda x: x["preco"], reverse=True)

            # Displaying substitute products in the desired style
            for product in substitutos:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: #262730;">
                    <h4>{product['nome_completo']} - {product['cod_prod']}</h4>
                    <p>{product['descricao']}</p>
                    <p>Preço: <strong><span style="color: #32B950;">R$ {product['preco']:.2f}</span></strong> | Margem: <strong><span style="color: #32B950;">{product['margem_lucro_bruto']:.2f}%</span></strong></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("Nenhum produto substituto encontrado.")
    else:
        st.error("Por favor, preencha tanto o ID do produto quanto o ID da loja.")
