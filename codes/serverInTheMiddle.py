import json
from socket import *
from library.lib import tirar_foto 
import base64
from datetime import datetime
from cryptography.fernet import Fernet

# Servidor responsável por receber mensagem do client.py e enviar ao server.py

## Configs de criptografia
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

## Configs do TCP serverInTheMiddle.py

serverMiddlePort = 14000
serverSocket = socket(AF_INET,SOCK_STREAM)   # AF_INET = IPv4, SOCK_STREAM = TCP
serverSocket.bind(('',serverMiddlePort))
serverSocket.listen(1)

def aquisicao_imagem():
    hour = datetime.now()
    
    if tirar_foto():
        with open("./tmp/image.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        print("Erro ao tirar a imagem")
        return -1

    # Criptografa a imagem
    encrypted_image = cipher.encrypt(encoded_string.encode())

    # Formata os dados para o envio
    data = {
        "image": encrypted_image.decode('utf-8'),
        "hour": hour.strftime("%Y-%m-%d %H:%M:%S.%f")
    }

    # Publica os dados no tópico MQTT
    return data

# Abre conexão com server.py
def abre_conexao():
    serverName = '192.168.56.1'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    data = aquisicao_imagem()
    if data != -1:
        data = json.dumps(data)
        clientSocket.sendall(str(data).encode())
        clientSocket.close()
        return True
    else:    
        clientSocket.close()
        return False

while True:
    connectionSocket, addr = serverSocket.accept()

    sentence = connectionSocket.recv(1024).decode()

    if sentence == "takePicture":
        if abre_conexao():
            print("Imagem publicada com sucesso")
            connectionSocket.send("Imagem publicada com sucesso".encode())
        else:
            print("Erro ao publicar imagem")
            connectionSocket.send("Erro ao publicar imagem".encode())
    else:
        print("Erro ao publicar imagem")
        connectionSocket.send("Erro ao publicar imagem".encode())
    connectionSocket.close()
