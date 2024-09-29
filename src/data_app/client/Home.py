import streamlit as st
from auth.auth import get_login_url, get_access_token, get_user_info

def show_login_screen():
    st.title("Bem-vindo ao Dashboard")
    st.write("Por favor, faça login para acessar seu dashboard personalizado.")

    login_url = get_login_url()

    st.markdown(
        """
        <style>
        .custom-button {
            display: inline-block;
            background-color: #FFFFFF;
            color: black;
            padding: 10px 20px;
            font-size: 16px; 
            border: none;
            border-radius: 5px;
            text-align: center;
            text-decoration: none; 
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .custom-button:hover {
            background-color: #FBF5F1; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f'<a href="{login_url}" class="custom-button">Fazer Login</a>', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="centered")

    query_params = st.query_params

    if 'code' in query_params:
        code = query_params['code']
        access_token = get_access_token(code)

        if access_token:
            user_info = get_user_info(access_token) 
            st.session_state.user_info = user_info  

            st.title("Dashboard Principal")
            st.write("Bem-vindo ao seu dashboard! Use o menu à esquerda para navegar.")
        else:
            st.error("Erro ao obter o token de acesso.")
    else:
        show_login_screen() 

if __name__ == "__main__":
    main()
