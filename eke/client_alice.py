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
    pubkey, privkey = rsa.newkeys(512)
    k_a = sym.encrypt(pubkey.n.to_bytes(64, 'big'), secret)
    print(f'k_a = {k_a}')
    client_socket.send(k_a)

    # stage 2: Bob chooses random number r_b and sends it to Alice
    k_b_p = client_socket.recv(1024)

    # stage 3: Alice and Bob exchange keys
    k_b = sym.decrypt(k_b_p, secret)
    print(f'k_b = {k_b}')
    k_session = rsa.decrypt(k_b, privkey)
    print(f'k_session = {k_session}')
    print(f'k_b = {k_b}')

    r_a = sym.generate_key()
    print(f'r_a = {r_a}')
    r_a_k = sym.encrypt(r_a, k_session)
    client_socket.send(r_a_k)

    # stage 4: Alice and Bob exchange r_a r_b
    r_a_k_b = client_socket.recv(1024)
    r_b_k = client_socket.recv(1024)

    # stage 5: Alice and Bob exchange r_a and r_b
    r_a_b = sym.decrypt(r_a_k_b, k_session)
    if r_a_b == r_a:
        print('r_a_b == r_a')
    else:
        print('r_a_b != r_a')
        print("Ключи не совпали")
        exit(0)
    r_b = sym.decrypt(r_b_k, k_session)
    r_b_k = sym.encrypt(r_b, k_session)
    client_socket.send(r_b_k)

    print('Работа с шифрованием закончена')
    print(f'r_a = {r_a}, r_b = {r_b}, k_session = {k_session}')

    # Write Alice's key to file
    with open('key_alice.txt', 'w') as f:
        f.write(f'{k_a=}, \n{r_a=}, \n{k_b=}, \n{r_b=}, \n{k_session=}')

    print('Завершение соединений...')
    client_socket.close()


if __name__ == '__main__':
    client_program()
