from services.substitutes_service import sugerir_substituto_com_estoque
import streamlit as st

st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Sugestão de produtos")
st.write("Informe o ID de um produto da compra para receber sugestão de um produto a ser vendido em conjunto, ou de um produto substituto.")

# Formulário para buscar produto substituto
col1, col2 = st.columns(2)
with col1:
    cod_prod = st.text_input("ID do produto", value="599019471098")
with col2:
    cod_loja = st.text_input("ID da loja", value="RJ_37")

# Botão para realizar a pesquisa
search = st.button("Enviar")

# Quando o botão é clicado, chama a função para buscar substitutos
if search:
    substitutos = sugerir_substituto_com_estoque(cod_prod, cod_loja)
    
    if isinstance(substitutos, str):
        st.error(substitutos)
    else:
        st.write(f"**Produto informado:** {substitutos[0]['nome_completo']} | Preço: R${substitutos[0]['preco']:.2f} | Margem: {substitutos[0]['margem_lucro_bruto']:.2f}%")
    
    # Ordenação dos produtos por margem ou preço
    order_by = st.selectbox("Ordenar por", ["Margem de lucro", "Preço"])
    
    if order_by == "Margem de lucro":
        substitutos = sorted(substitutos, key=lambda x: x["margem_lucro_bruto"], reverse=True)
    elif order_by == "Preço":
        substitutos = sorted(substitutos, key=lambda x: x["preco"], reverse=True)
    
    # Exibição dos produtos substitutos
    for product in substitutos:
        st.markdown(f"""
        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: #262730;">
            <h4>{product['nome_completo']} - {product['cod_prod']}</h4>
            <p>{product['descricao']}</p>
            <p>Preço: <strong><span style="color: #32B950;">R$ {product['preco']:.2f}</span></strong> | Margem: <strong><span style="color: #32B950;">{product['margem_lucro_bruto']:.2f}%</span></strong></p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.write("Nenhum produto encontrado. Clique em 'Enviar' para iniciar a pesquisa.")
