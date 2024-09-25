from services.margin_service import get_similar_product_by_margin, get_product_categories, get_product_subcategories, get_product_brands
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

st.title("Análise de margens de lucro")
st.write("Análise de produtos com maior margem de acordo com informações fornecidas.")

categories = get_product_categories()
subcategories = get_product_subcategories()
brands = get_product_brands()

categories = ["Selecionar"] + categories if categories else ["Selecionar"]
subcategories = ["Selecionar"] + subcategories if subcategories else ["Selecionar"]
brands = ["Selecionar"] + brands if brands else ["Selecionar"]

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Categoria", categories)
with col2:
    subcategory = st.selectbox("Sub-categoria", subcategories)

brand = st.selectbox("Marca", brands)

col3, col4 = st.columns(2)
with col3:
    min_price = st.text_input("Preço Mínimo", value="0", key="min_price")
with col4:
    max_price = st.text_input("Preço Máximo", value="50", key="max_price")

description = st.text_input("Especificação", "Exemplo: Batom rosa com brilho")

search = st.button("Buscar")

if search:
    try:
        min_price_value = int(min_price)
        max_price_value = int(max_price)
    except ValueError:
        st.error("Por favor, insira valores válidos para os preços.")
        min_price_value, max_price_value = 0, 50

    st.session_state["products"] = get_similar_product_by_margin(description, category, subcategory, brand, max_price_value, min_price_value)

if "products" in st.session_state and st.session_state["products"]:
    products = st.session_state["products"]

    st.write("###")
    
    order_by = st.selectbox("Ordenar por", ["Margem", "Preço"])

    if order_by == "Margem":
        products = sorted(products, key=lambda x: x["margem_lucro_bruto"], reverse=True)
    elif order_by == "Preço":
        products = sorted(products, key=lambda x: x["preco"], reverse=True)
    
    for product in products:
        st.markdown(f"""
        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: #262730;">
            <h4>{product['nome_completo']} - {product['cod_prod']}</h4>
            <p>{product['descricao']}</p>
            <p>Preço: <strong><span style="color: #32B950;">R$ {product['preco']:.2f}</span></strong> | Margem: <strong><span style="color: #32B950;">{product['margem_lucro_bruto']:.2f}%</span></strong></p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("Nenhum produto encontrado. Clique em 'Buscar' para iniciar uma pesquisa.")
