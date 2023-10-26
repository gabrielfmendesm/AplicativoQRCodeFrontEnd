import streamlit as st
import requests
from PIL import Image
from datetime import time

# Defina um ícone personalizado para a página
st.set_page_config(
    page_title="Painel de Admin",
    page_icon=":key:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Estilize o título da página
st.title("Bem-vindo ao Painel de Administração")

# Criação das abas
menu = st.sidebar.selectbox("Selecione uma opção:", ["Cadastrar Usuário", "Cadastrar Porta", "Testar Acesso"])

# Aba "Cadastrar Usuário"
if menu == "Cadastrar Usuário":
    st.header("Cadastro de Usuário")

    # Campos de entrada para o login e o nome do usuário
    login_usuario = st.text_input("Login de Usuário")
    nome_usuario = st.text_input("Nome de Usuário")

    # Campo de entrada para o nível de permissão do usuário
    nivel_usuario = st.selectbox("Nível de Permissão", [1, 2, 3, 4, 5])

    # Botão com estilo personalizado
    if st.button("Cadastrar Usuário", key="cadastro_usuario"):
        if login_usuario and nome_usuario:
            # Realize a requisição para o backend
            
            response = requests.post(f"http://127.0.0.1:5000/usuario", json={"login": login_usuario, "nome": nome_usuario, "permissao": nivel_usuario})
            if response.status_code == 201:
                st.success("Usuário cadastrado com sucesso.")
            elif response.status_code == 400:
                st.warning("Usuário já cadastrado.")
            else:
                st.error("Erro ao cadastrar usuário. Tente novamente mais tarde.")
        else:
            st.warning("Por favor, preencha todos os campos.")

# Aba "Cadastrar Porta"
if menu == "Cadastrar Porta":
    st.header("Cadastro de Porta")

    # Campos de entrada para o número do prédio e da sala
    numero_predio = st.text_input("Número do Prédio")
    numero_sala = st.text_input("Número da Sala")

    # Campo de entrada para o nível de permissão de acesso
    nivel_acesso = st.selectbox("Nível de Permissão de Acesso", [1, 2, 3, 4, 5])

    # Campo de entrada para exceções de acesso (opcional)
    excecoes_acesso = st.text_input("Exceções de Acesso (opcional)")

    # Botão com estilo personalizado
    if st.button("Cadastrar Porta", key="cadastro_porta"):
        if numero_predio and numero_sala:
            # Realize a requisição para o backend
            
            response = requests.post(f"http://127.0.0.1:5000/porta", json={"predio": int(numero_predio), "sala": int(numero_sala), "permissao": nivel_acesso, "excecoes": excecoes_acesso.split(", ")})
            
            if response.status_code == 201:
                st.success("Porta cadastrada com sucesso.")
            elif response.status_code == 400:
                st.warning("Porta já cadastrada.")
            else:
                st.error("Erro ao cadastrar porta. Tente novamente mais tarde.")
        else:
            st.warning("Por favor, preencha todos os campos.")

# Divisor para separar seções
st.write("---")

# Rodapé com informações adicionais
st.markdown("Desenvolvido por [Seu Nome]")
st.markdown("[GitHub](https://github.com/seu-usuario) | [LinkedIn](https://www.linkedin.com/in/seu-usuario)")

# Adicione cores de fundo e estilização de texto conforme necessário para destacar informações importantes.

