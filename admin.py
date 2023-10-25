import streamlit as st
import requests

# Título do aplicativo
st.title("Painel de Admin")

# Criação das abas
menu = st.sidebar.selectbox("Selecione uma opção:", ["Cadastrar Usuário", "Cadastrar Porta", "Testar Acesso"])

# Aba "Cadastrar Usuário"
if menu == "Cadastrar Usuário":
    # Campo de entrada para o login de usuário
    login_usuario = st.text_input("Digite o login de usuário:")

    # Campo de entrada para o nome de usuário
    nome_usuario = st.text_input("Digite o nome de usuário:")

    # Campo de entrada para o nível de permisão de usuário
    nivel_usuario = st.selectbox("Selecione o nível de permissão de usuário:", [1, 2, 3, 4, 5])

    # Botão para cadastrar usuário
    if st.button("Cadastrar Usuário"):
        # Se o login de usuário for infomado, então:
        if login_usuario:
            # Se o nome de usuário for infomado, então:
            if nome_usuario:
                # Realiza a requisição para o backend
                response = requests.post(f"http://127.0.0.1:5000/usuario", json={"login": login_usuario, "nome": nome_usuario, "permissao": nivel_usuario})

                # Se a resposta for 201, então:
                if response.status_code == 201:
                    st.success("Usuário cadastrado com sucesso.")

                # Se a resposta for 400, então:
                elif response.status_code == 400:
                    st.warning("Usuário já cadastrado.")

                # Se a resposta for diferente de 201 e 400, então:
                else:
                    st.warning("Erro ao cadastrar usuário.")

            # Se o nome de usuário não for informado, então:
            else:
                st.warning("Por favor, insira um nome de usuário para cadastrar.")

        # Se o login de usuário não for informado, então:
        else:
            st.warning("Por favor, insira um login de usuário para cadastrar.")

# Aba "Cadastrar Porta"
if menu == "Cadastrar Porta":
    # Campo de entrada para o número do prédio
    numero_predio = st.text_input("Digite o número do prédio:")

    # Campo de entrada para o número da sala
    numero_sala = st.text_input("Digite o número da sala:")

    # Campo de entrada para o nível de permisão de acesso
    nivel_acesso = st.selectbox("Selecione o nível de permissão de acesso:", [1, 2, 3, 4, 5])

    # Campo de entrada para escrever as exceções de acesso (opcional)
    excecoes_acesso = st.text_input("Digite as exceções de acesso (opcional):")

    # Convertendo as exceções de acesso para lista
    excecoes_acesso = excecoes_acesso.split(", ")

    # Botão para cadastrar porta
    if st.button("Cadastrar Porta"):
        # Se o número do prédio for infomado, então:
        if numero_predio:
            # Se o número da sala for infomado, então:
            if numero_sala:
                # Realiza a requisição para o backend
                response = requests.post(f"http://127.0.0.1:5000/porta", json={"predio": int(numero_predio), "sala": int(numero_sala), "permissao": nivel_acesso, "excecoes": excecoes_acesso})

                # Se a resposta for 201, então:
                if response.status_code == 201:
                    st.success("Porta cadastrada com sucesso.")

                # Se a resposta for 400, então:
                elif response.status_code == 400:
                    st.warning("Porta já cadastrada.")

                # Se a resposta for diferente de 201 e 400, então:
                else:
                    st.warning("Erro ao cadastrar porta.")

            # Se o número da sala não for informado, então:
            else:
                st.warning("Por favor, insira um número da sala para cadastrar.")

        # Se o número do prédio não for informado, então:
        else:
            st.warning("Por favor, insira um número do prédio para cadastrar.")
