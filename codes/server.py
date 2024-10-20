import json
from socket import *
import base64
from datetime import datetime
from cryptography.fernet import Fernet

# Servidor responsável por receber a imagem do serverInTheMiddle.py e armazenar em database

## Configs de criptografia
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

## Configs do TCP server.py

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)   # AF_INET = IPv4, SOCK_STREAM = TCP
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()

    data = b""
    while True:
        chunk = connectionSocket.recv(4096)  # Lê blocos de 4096 bytes
        if not chunk:
            break
        data += chunk

    print("Received: ", len(data), "B")
    print("Received: ", len(data) / 1024, "KB")

    data = json.loads(data.decode('utf-8'))
        
    # Descriptografa a imagem
    encrypted_image = data["image"].encode()
    decrypted_image = cipher.decrypt(encrypted_image).decode('utf-8')

    # Decodifica a imagem de base64
    decoded_image = base64.b64decode(decrypted_image)

    # Salva a imagem no disco com timestamp
    hour_now = datetime.now()
    with open(f"database/image{hour_now.strftime('%Y%m%d_%H%M%S')}.png", "wb") as image_file:
        image_file.write(decoded_image)

    request_hour = datetime.strptime(data["hour"], "%Y-%m-%d %H:%M:%S.%f")
    print(f"Imagem recebida e salva com sucesso. Tempo de transmissão: {hour_now - request_hour}")

    connectionSocket.close()
