import socket
import time

import rsa

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

    # Diffie-Hellman Ephemeral Key Exchange (DH-EKE) work
    # stage 1: Alice choses random number r_a and sends it to Bob
    with open('secret.bin', 'rb') as f:
        secret = f.read()
    k_a = client_socket.recv(1024)
    print(f'k_a = {k_a}')

    # stage 2: Bob chooses random number r_b and sends it to Alice
    pubkey = sym.decrypt(k_a, secret)
    k_session = sym.generate_key()
    print(f'k_session = {k_session}')

    # repair key structure
    pubkey_t, _ = rsa.newkeys(512)
    pubkey_t.n = int.from_bytes(pubkey, 'big')
    pubkey = pubkey_t

    k_b = rsa.encrypt(k_session, pubkey)
    print(f'k_b = {k_b}')
    k_b_p = sym.encrypt(k_b, secret)
    client_socket.send(k_b_p)

    # stage 3: Alice and Bob exchange keys
    r_a_k = client_socket.recv(1024)

    # stage 4: Alice and Bob exchange r_a and r_b
    r_a = sym.decrypt(r_a_k, k_session)
    r_b = sym.generate_key()
    print(f'r_a = {r_a}, r_b = {r_b}')
    r_b_k = sym.encrypt(r_b, k_session)
    client_socket.send(r_a_k)
    time.sleep(1)
    client_socket.send(r_b_k)

    # stage 5: Alice and Bob exchange r_a and r_b
    r_b_k_a = client_socket.recv(1024)
    r_b_a = sym.decrypt(r_b_k_a, k_session)
    if r_b_a == r_b:
        print('r_b_a == r_b')
    else:
        print('r_b_a != r_b')
        print('Ключи не совпали')
        exit(0)

    print('Работа с шифрованием окончена')
    print(f'r_a = {r_a}, r_b = {r_b}, k_session = {k_session}')

    # Write Bob's key to file
    with open('key_bob.txt', 'w') as f:
        f.write(f'{k_a=}, \n{r_a=}, \n{k_b=}, \n{r_b=}, \n{k_session=}')

    print('Завершение соединений...')
    client_socket.close()


if __name__ == '__main__':
    client_program()
