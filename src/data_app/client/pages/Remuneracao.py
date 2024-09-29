import streamlit as st
import pandas as pd
import plotly.express as px
from services.view_service import fetch_data

if 'user_info' in st.session_state:
    st.title("Desempenho da loja")

    # Input do usuário
    store_id_input = st.text_input("Digite o ID da loja (ex: RJ_37):")
    store_id = store_id_input.strip().upper()  # Remove espaços e ignora maiúsculas/minúsculas

    # Seletor de mês e ano
    mes = st.selectbox("Selecione o mês", ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
    mes_dict = {
        'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
        'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
        'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
    }
    mes_selecionado = mes_dict[mes]

    ano = st.selectbox("Selecione o ano", [2022, 2023, 2024])

    # Função para buscar dados da view
    def filter_remuneracao(store_id, mes, ano):
        endpoint = "remuneracao"
        df = fetch_data(endpoint)
        df_filtrado = df[(df['t.cod_loja'] == store_id) & (df['t.mes'] == mes) & (df['t.ano'] == ano)]
        return df_filtrado

    if st.button("Buscar Desempenho"):
        if store_id and mes_selecionado and ano:
            # Buscar os dados filtrados da view
            df_remuneracao = filter_remuneracao(store_id, mes_selecionado, ano)

            if not df_remuneracao.empty:
                st.write(df_remuneracao)

                # Criando um DataFrame para os valores de 'target' e 'total_vendas'
                desempenho_loja = pd.DataFrame({
                    'Métrica': ['Target', 'Total Vendas'],
                    'Valor': [df_remuneracao['target'].values[0], df_remuneracao['total_vendas'].values[0]]
                })

                # Gráfico 1: Comparação entre target e vendas realizadas
                fig_target = px.bar(desempenho_loja, x='Métrica', y='Valor', title=f'Desempenho da Loja {store_id}')
                st.plotly_chart(fig_target)

                # Usando 'l.regiao' no lugar de 'regiao'
                if 'l.regiao' in df_remuneracao.columns:
                    # Gráfico 2: Comparação com outras lojas da região
                    region = df_remuneracao['l.regiao'].values[0]
                    df_regiao = fetch_data("remuneracao")
                    df_regiao_filtrado = df_regiao[(df_regiao['l.regiao'] == region) & (df_regiao['t.mes'] == mes_selecionado) & (df_regiao['t.ano'] == ano)]

                    fig_regiao = px.bar(df_regiao_filtrado, x='t.cod_loja', y='total_vendas', title=f'Comparação de Vendas na Região {region}')
                    st.plotly_chart(fig_regiao)
                else:
                    st.warning("A coluna 'l.regiao' não está disponível nos dados.")
            else:
                st.warning("Nenhum dado encontrado para os filtros selecionados.")
        else:
            st.warning("Por favor, preencha todos os campos.")
else:
    st.write("Você precisa estar autenticado para acessar esta página.")