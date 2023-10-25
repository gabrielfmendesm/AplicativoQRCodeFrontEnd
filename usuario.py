import streamlit as st
import requests
import io
from PIL import Image


# Título do aplicativo
st.title("Gerador de QR Code")

# Campo de entrada para o login de usuário
login_usuario = st.text_input("Digite o login de usuário:")

# Botão para gerar QR Code
if st.button("Gerar QR Code"):
    # Se o login de usuário for infomado, então:
    if login_usuario:
        # Realiza a requisição para o backend
        response = requests.get(f"http://127.0.0.1:5000/qrcode/usuario/{login_usuario}")

        # Se a resposta for 200, então:
        if response.status_code == 200:
            # Carrega a imagem do QR Code a partir dos dados da resposta
            qr_code_data = response.content
            img = Image.open(io.BytesIO(qr_code_data))

            # Exibe o QR Code
            st.markdown(f"QR Code gerado para o usuário: {login_usuario}")
            st.image(img, use_column_width=True)
        
        # Se a resposta for 404, então:
        elif response.status_code == 404:
            st.warning(response.json()["mensagem"])

        # Se a resposta for diferente de 200 e 404, então:
        else:
            st.warning("Erro ao gerar o QR Code.")
    
    # Se o login de usuário não for informado, então:
    else:
        st.warning("Por favor, insira um nome de usuário para gerar o QR Code.")