import streamlit as st
import pandas as pd
import altair as alt
from services.view_service import fetch_data

if 'user_info' in st.session_state:
    st.title("Region View Dashboard")
    try:
        region_data = fetch_data("regions") 
        if region_data is None or region_data.empty:
            st.error("Nenhum dado foi retornado do servidor.")
        else:
            df_filtered = region_data.copy()

            st.header("Filtros")

            regioes = ['Todas'] + df_filtered['regiao'].unique().tolist()
            region = st.selectbox("Selecione a Região", regioes)
            if region != 'Todas':
                df_filtered = df_filtered[df_filtered['regiao'] == region]

            diretorias = ['Todas'] + df_filtered['diretoria'].unique().tolist()
            diretoria = st.selectbox("Selecione a Diretoria", diretorias)
            if diretoria != 'Todas':
                df_filtered = df_filtered[df_filtered['diretoria'] == diretoria]

            if not df_filtered.empty:
                st.subheader("Faturamento por região")

                df_filtered['mes'] = pd.to_datetime(df_filtered['mes'])

                faturamento_mes_regiao = df_filtered[['mes', 'regiao', 'faturamento_total']].drop_duplicates()

                chart_faturamento_mes = alt.Chart(faturamento_mes_regiao).mark_line(point=True).encode(
                    x=alt.X('mes:T', title='Mês'),
                    y=alt.Y('faturamento_total:Q', title='Faturamento (R$)', axis=alt.Axis(format='~s')),
                    color='regiao:N', 
                    tooltip=['mes:T', 'regiao:N', 'faturamento_total:Q']
                ).properties(
                    width=700,
                    height=400,
                    title="Faturamento por região"
                ).interactive()

                st.altair_chart(chart_faturamento_mes)

                st.subheader("Ticket médio por região")

                ticket_medio_regiao_mes = df_filtered[['mes', 'regiao', 'ticket_medio']].drop_duplicates()

                chart_ticket_medio = alt.Chart(ticket_medio_regiao_mes).mark_line(point=True).encode(
                    x=alt.X('mes:T', title='Mês'),
                    y=alt.Y('ticket_medio:Q', title='Ticket Médio (R$)', axis=alt.Axis(format='~s')),
                    color='regiao:N',  
                    tooltip=['mes:T', 'regiao:N', 'ticket_medio:Q']
                ).properties(
                    width=700,
                    height=400,
                    title="Ticket médio por região"
                ).interactive()

                st.altair_chart(chart_ticket_medio)

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os dados: {str(e)}")
else:
    st.write("Você precisa estar autenticado para acessar esta página.")
