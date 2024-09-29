import streamlit as st
from services.cross_sell_service import get_similar_products_by

# Custom CSS para formatação (o mesmo que no substitutos.py)
st.markdown("""
    <style>
    /* Botão de envio */
    .stButton button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
    }

    .stButton button:hover {
        background-color: #FF3333;
        color: white;
    }

    /* Caixa de informações do produto informado */
    .product-info-box {
        background-color: #1e3a5f;
        padding: 15px;
        border-radius: 8px;
        color: #d4d8e4;
        font-size: 16px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* Título do produto */
    .product-name {
        font-weight: bold;
        font-size: 20px;
        color: #d4d8e4;
    }

    /* Preço e margem */
    .product-price, .product-margin {
        color: #32B950;
        font-weight: bold;
    }

    /* Descrição do produto */
    .product-description {
        margin-top: 10px;
        color: #a0a0a0;
        font-size: 14px;
    }

    /* Estilização da sugestão de produtos */
    div.product-card {
        border: 1px solid #3a3b3c;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        background-color: #262730;
    }

    h4.product-name {
        font-weight: bold;
        color: #d4d8e4;
        font-size: 18px;
    }

    p.product-price, p.product-margin {
        color: #32B950;
        font-weight: bold;
    }

    /* Caixa de informações de Cross-Sell */
    .blue-info-box {
        background-color: #1e3a5f;
        padding: 10px;
        border-radius: 8px;
        color: #d4d8e4;
        font-size: 14px;
        border-left: 5px solid #5d9ce5;
        margin-bottom: 20px;
    }

    /* Caixa de input */
    .css-1lcbmhc {
        background-color: #262730 !important;
        color: white !important;
    }

    /* Centralizando o dropdown */
    .css-1lcbmhc {
        text-align: center;
    }

    </style>
""", unsafe_allow_html=True)

# Título da Página
st.title("Sugestão de cross-sell")
st.write("Informe o ID de um produto da compra para receber sugestões de produtos frequentemente vendidos em conjunto.")

# Caixa de informações para Cross-Sell
st.markdown("""
<div class="blue-info-box">
    <p>💡 <strong>Para cross-sell</strong>, são considerados os produtos mais vendidos em conjunto com o item informado.</p>
</div>
""", unsafe_allow_html=True)

# Formulário de entrada para ID do produto e ID da loja
col1, col2 = st.columns(2)
with col1:
    cod_prod = st.text_input("ID do produto", value="")
with col2:
    cod_loja = st.text_input("ID da loja", value="")

# Botão para enviar
search = st.button("Enviar")

# Processamento da entrada e exibição dos resultados
if search:
    if cod_prod and cod_loja:
        cross_sell_products = get_similar_products_by(cod_loja, cod_prod)

        # Simulando a recuperação das informações do produto
        if isinstance(cross_sell_products, list) and cross_sell_products:
            produto_informado = cross_sell_products[0]
            produto_nome = produto_informado.get('nome', 'Produto sem nome')
            descricao = produto_informado.get('descricao', 'Descrição indisponível')
            codigo_produto = produto_informado.get('cod_loja', 'ID não disponível')

            # Exibindo o produto informado
            st.markdown(f"""
            <div class="product-info-box">
                <strong>Produto informado</strong> <br>
                {produto_nome} <br> ID da Loja: <strong>{codigo_produto}</strong>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("Produtos sugeridos para cross-sell:")

            # Opções de ordenação
            order_by = st.selectbox("Ordenar por", ["Frequência de venda", "Preço"])

            if order_by == "Frequência de venda":
                cross_sell_products = sorted(cross_sell_products, key=lambda x: x.get("frequency", 0), reverse=True)
            elif order_by == "Preço":
                cross_sell_products = sorted(cross_sell_products, key=lambda x: float(x.get("preco", "R$ 0,00").replace("R$ ", "").replace(",", ".")), reverse=True)

            # Exibindo os produtos cross-sell
            for product in cross_sell_products:
                st.markdown(f"""
                <div class="product-card">
                    <h4 class="product-name">{product.get('nome', 'Sem nome')} - {product.get('cod_loja', 'Sem ID')}</h4>
                    <p>{product.get('descricao', 'Sem descrição')}</p>
                    <p>Preço: <span class="product-price">R$ {product.get('preco', '0,00')}</span> | Frequência: <span class="product-margin">{product.get('frequency', 'Sem frequência')}</span></p>
            </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Nenhum produto de cross-sell encontrado ou houve um erro.")
    else:
        st.error("Por favor, preencha tanto o ID do produto quanto o ID da loja.")
