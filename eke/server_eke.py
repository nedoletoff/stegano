import socket
import threading
import time


def get_message(conn):
    data = conn.recv(1024)
    #print('Получено: ' + data.decode('utf-8'))
    return data


def send_message(conn, message, name):
    print('Отправлено от ' + name + ': ', end='')
    print(message)
    conn.send(message)


def exchange_messages(conn1, conn2, name):
    while True:
        message = get_message(conn1)
        send_message(conn2, message, name)
        if not message:
            print('Соединение закрыто ' + name)
            time.sleep(5)
            conn1.close()
            conn2.close()
            exit(-1)


def server_program():
    host = socket.gethostname()
    port = 8080

    # Подключение к серверу

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    conns = []

    print(f'Сервер запущен. Ожидание подключений...')
    conn1, address = server_socket.accept()
    conns.append(conn1)
    print(f'Подключение от {address} Alice установлено.')
    conn1.send('Соединение установлено'.encode())

    conn2, address = server_socket.accept()
    conns.append(conn2)
    print(f'Подключение от {address} Bob установлено.')
    conn2.send('Соединение установлено'.encode())

    threads = [threading.Thread(target=exchange_messages, args=(conns[0], conns[1], 'Alice')),
               threading.Thread(target=exchange_messages, args=(conns[1], conns[0], 'Bob'))]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('Завершение соединений...')
    for conn in conns:
        conn.close()
    server_socket.close()


if __name__ == '__main__':
    server_program()
