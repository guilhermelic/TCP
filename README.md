# Captura e envio de foto utilizando TCP

## Funcionamento

Temos um servidor (server.py) que receberá as imagens e armazenará a imagem em .\database, calculando o tempo necessário para transmissão, bem como o tamanho da mensagem.
Temos um servidor intermediário (serverInTheMiddle.py) que captura a imagem e envia ao servidor principal. Nesse caso, se comporta tanto como servidor quanto como cliente (há duas conexões).
Temos o cliente (client.py) que envia a mensagem ("takePicture") ao servidor intermediário, para captura da foto. 

## Como utilizar

Há três arquivos de códigos: client.py, server.py e serverInTheMiddle.py.
Para rodar os arquivos, certifique-se de instalar as dependências em requirements.txt.

Rode primeiramente o serverInTheMiddle.py:

```py serverInTheMiddle.py ```

Rode o server.py:

``` py server.py ```

Por fim, para capturar a imagem, rode:

``` py client.py ```

