import socket
from Crypto.Cipher import AES

import sym



def client_program():
    host = socket.gethostname()
    port = 8080

    # Подключение к серверу

    client_socket = socket.socket()
    client_socket.connect((host, port))

    print('Подключено к серверу ' + host + ' на порту ' + str(port))
    data = client_socket.recv(1024).decode()
    print(data)


if __name__ == '__main__':
    client_program()
