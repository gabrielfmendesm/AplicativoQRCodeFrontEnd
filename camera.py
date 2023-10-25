import streamlit as st
import cv2
import numpy as np
import streamlit as st
from PIL import Image
import numpy as np

# Título do aplicativo
st.title("Teste de Câmera")

# Campo de entrada para o número do prédio e da sala
numero_predio = st.text_input("Digite o número do prédio:")
numero_sala = st.text_input("Digite o número da sala:")

# Função para detectar e ler código QR em uma imagem
def detect_qr_code(cv2_img):
    # Converte a imagem em escala de cinza
    gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)

    # Inicializa o detector de código QR
    qr_code_detector = cv2.QRCodeDetector()

    # Detecta os códigos QR na imagem
    decoded_info, points, _ = qr_code_detector.detectAndDecodeMulti(gray)

    if decoded_info:
        for info in decoded_info:
            st.success(f'QR Code Data: {info}')
            
            # Desenha um retângulo ao redor do código QR na imagem
            for point in points:
                for i in range(4):
                    cv2.line(cv2_img, tuple(point[i]), tuple(point[(i+1)%4]), (0, 255, 0), 3)

    return cv2_img

st.title("Detecção de QR Code na Câmera")

img_file_buffer = st.camera_input("Tire uma foto")

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    st.write("Tipo da imagem:", type(cv2_img))
    st.write("Formato da imagem:", cv2_img.shape)

    img_with_qr_code = detect_qr_code(cv2_img)

    st.image(img_with_qr_code, channels="BGR")
