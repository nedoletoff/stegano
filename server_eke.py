import socket
from Crypto.Cipher import AES


p = 13
gen = [2, 6, 11, 7]
block_size = 16

def server_program():
    host = socket.gethostname()
    port = 8080

    # Подключение к серверу

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    print(f'Сервер запущен. Ожидание подключений...')
    conn1, address = server_socket.accept()
    print(f'Подключение от {address} установлено.')
    conn1.send('Соединение установлено'.encode())

    #




if __name__ == '__main__':
    server_program()
