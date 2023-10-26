import streamlit as st
import requests
import json
import cv2

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
    # Título da aba
    st.header("Cadastro de Usuário")

    # Campo de entrada para o login e nome de usuário
    login_usuario = st.text_input("Login de usuário:")
    nome_usuario = st.text_input("Nome de usuário:")

    # Campo de entrada para o nível de permisão de usuário
    nivel_usuario = st.selectbox("Nível de permissão de usuário:", [1, 2, 3, 4, 5])

    # Botão para cadastrar usuário
    if st.button("Cadastrar Usuário", key="cadastro_usuario"):
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
                    st.error("Erro ao cadastrar usuário. Tente novamente mais tarde.")

            # Se o nome de usuário não for informado, então:
            else:
                st.warning("Por favor, insira um nome de usuário para cadastrar.")

        # Se o login de usuário não for informado, então:
        else:
            st.warning("Por favor, insira um login de usuário para cadastrar.")

# Aba "Cadastrar Porta"
if menu == "Cadastrar Porta":
    # Título da aba
    st.header("Cadastro de Porta")

    # Campos de entrada para o número do prédio e da sala
    numero_predio = st.text_input("Número do prédio:")
    numero_sala = st.text_input("Número da sala:")

    # Campo de entrada para o nível de permisão de acesso
    nivel_acesso = st.selectbox("Nível de permissão de acesso:", [1, 2, 3, 4, 5])

    # Campo de entrada para escrever as exceções de acesso (opcional)
    excecoes_acesso = st.text_input("Exceções de acesso (opcional):")

    # Convertendo as exceções de acesso para lista
    excecoes_acesso = excecoes_acesso.split(", ")

    # Botão com estilo personalizado
    if st.button("Cadastrar Porta", key="cadastro_porta"):
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
                    st.error("Erro ao cadastrar porta. Tente novamente mais tarde.")

            # Se o número da sala não for informado, então:
            else:
                st.warning("Por favor, insira um número da sala para cadastrar.")

        # Se o número do prédio não for informado, então:
        else:
            st.warning("Por favor, insira um número do prédio para cadastrar.")

# Aba "Testar Acesso"
if menu == "Testar Acesso":
    # Título da aba
    st.header("Testar Acesso")

    # Campo de entrada para o número do prédio
    numero_predio = st.text_input("Digite o número do prédio:")

    # Campo de entrada para o número da sala
    numero_sala = st.text_input("Digite o número da sala:")

    # Botão com estilo personalizado
    if st.button("Testar Acesso", key="testar_acesso"):
        # Se o número do prédio for informado, então:
        if numero_predio:
            # Se o número da sala for infomado, então:
            if numero_sala:
                # Variável para armazenar os dados do QR Code
                qr_code_data = None
                
                # Abre a câmera
                cap = cv2.VideoCapture(0)

                # Loop para capturar o frame da câmera
                while True:
                    # Captura o frame da câmera
                    ret, frame = cap.read()
                    
                    # Se não conseguir acessar câmera, então:
                    if not ret:
                        st.write("Erro ao acessar a câmera.")
                        break
                    
                    # Instancia o detector de QR Code
                    detector = cv2.QRCodeDetector()

                    # Detecta Code
                    data, vertices, _ = detector.detectAndDecode(frame)

                    # Se os dados do QR Code forem detectados, então:
                    if data:
                        st.write("Código QR detectado:")
                        st.image(frame, channels="BGR", use_column_width=True)

                        # Tenta decodificar o JSON do QR Code
                        try:
                            # Recebe os dados do QR Code
                            qr_code_data = json.loads(data)

                            # Recebe login do usuário e armazena na variável
                            login_usuario = qr_code_data.get("login", None)
                        
                        # Se não conseguir decodificar o JSON do QR Code, então:
                        except json.JSONDecodeError:
                            st.warning("Erro ao decodificar o JSON do QR Code.")
                            qr_code_data = None
                            login_usuario = None
                        break
                
                # Fecha a câmera
                cap.release()

                # Se o login do usuário for informado, então:
                if login_usuario:
                    # Realiza a requisição para o backend
                    response = requests.get(f"http://127.0.0.1:5000/acesso/usuario/{login_usuario}/predio/{numero_predio}/sala/{numero_sala}")

                    # Se a resposta for 200, então:
                    if response.status_code == 200:
                        st.success("Acesso permitido.")

                    # Se a resposta for 403, então:
                    elif response.status_code == 403:
                        st.warning("Acesso negado.")

                    # Se a resposta for diferente de 200 e 403, então:
                    else:
                        st.warning("Porta não encontrada.")
                
                # Se o login do usuário não foi detectado, então:
                else:
                    st.warning("Por favor, insira um QR Code válido.")
            
            # Se o número da sala não for informado, então:
            else:
                st.warning("Por favor, insira um número da sala para testar acesso.")
        
        # Se o número do prédio não for informado, então:
        else:
            st.warning("Por favor, insira um número do prédio para testar acesso.")

if menu == "Relatórios":
    st.header("Relatórios de Acesso")
    data = st.selectbox("Data", ['2023-10-26'])
    # Campos de entrada para o número do prédio e da sala
    numero_predio = st.text_input("Número do Prédio")
    numero_sala = st.text_input("Número da Sala")
    
    # Botão com estilo personalizado
    if st.button("Gerar relatório", key="gera_relatorios"):
        if numero_predio and numero_sala:
            # Realize a requisição GET para o backend
            
            response = requests.get(f"http://127.0.0.1:5000/relatorios", json={"data": data, "predio": numero_predio, "sala": numero_sala})
            
            if response.status_code == 200:
                data = response.json()
                acessos_permitidos = data["quantidade_acessos_permitidos"]
                acessos_negados = data["quantidade_acessos_negados"]
                st.success(f"{acessos_permitidos} acessos permitidos e {acessos_negados} negados")
            elif response.status_code == 400:
                st.warning("Relatório não encontrado.")
            else:
                st.error("Erro ao gerar relatório. Tente novamente mais tarde.")
        else:
            st.warning("Por favor, preencha todos os campos.")

# Divisor para separar seções
st.write("---")

# Rodapé com informações adicionais
st.markdown("Desenvolvido por [Seu Nome]")
st.markdown("[GitHub](https://github.com/seu-usuario) | [LinkedIn](https://www.linkedin.com/in/seu-usuario)")

# Adicione cores de fundo e estilização de texto conforme necessário para destacar informações importantes.