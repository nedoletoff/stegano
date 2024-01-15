import socket
import threading
import time

import sym

working = True


def get_message(conn):
    global working
    while working:
        data = conn.recv(1024)
        print('Получено: ' + data.decode('utf-8'))
        if data.decode('utf-8') == 'exit':
            working = False
            break
        time.sleep(1)


def send_message(conn):
    global working
    while working:
        message = input('Enter message: ')
        print('Отправлено: ' + message)
        conn.send(message.encode('utf-8'))
        if message == 'exit':
            working = False
            break


def client_program():
    host = socket.gethostname()
    port = 8080

    # Подключение к серверу

    client_socket = socket.socket()
    client_socket.connect((host, port))

    print('Подключено к серверу ' + host + ' на порту ' + str(port))
    data = client_socket.recv(1024).decode()
    print(data)

    read_thread = threading.Thread(target=get_message, args=(client_socket,))
    write_thread = threading.Thread(target=send_message, args=(client_socket,))

    read_thread.start()
    write_thread.start()

    read_thread.join()
    write_thread.join()

    print('Завершение соединений...')
    client_socket.close()


if __name__ == '__main__':
    client_program()
