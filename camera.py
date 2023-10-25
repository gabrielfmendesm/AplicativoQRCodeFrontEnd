import streamlit as st
import cv2
from pyzbar.pyzbar import decode

# Título do aplicativo
st.title("Detecção de QR Code com Streamlit e OpenCV")

# Função para abrir a câmera e aguardar um QR Code
def capture_qr_code():
    cap = cv2.VideoCapture(0)  # 0 é o índice da câmera padrão (pode variar)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Decodifica o QR Code se estiver presente na imagem
        decoded_objects = decode(frame)

        if decoded_objects:
            st.image(frame, channels="BGR", use_column_width=True)
            st.write("QR Code detectado:", decoded_objects[0].data.decode("utf-8"))
            break

    cap.release()

# Botão para iniciar a detecção de QR Code
if st.button("Aguardar QR Code"):
    capture_qr_code()
