from Crypto.Cipher import AES
import hashlib as hasher

p = 13
gen = [2, 6, 11, 7]
block_size = 16
extra = ' '


def pad(s: str) -> str:
    return s + (block_size - len(s) % block_size) * extra


def encrypt_str(message: str, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    p_message = pad(str(message))
    return cipher.encrypt((p_message.encode('utf-8')))


def encrypt(message: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(message)


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)


def generate_key() -> bytes:
    return hasher.sha256(str(p).encode()).digest()


def test_encrypt_decrypt(message):
    key = generate_key()
    ciphertext = encrypt_str(message, key)
    return decrypt(ciphertext, key)


def tests():
    message = 'Hello, World!'
    print(message)
    print(test_encrypt_decrypt(message))


if __name__ == '__main__':
    with open('secret.bin', 'wb') as f:
        f.write(generate_key())
    tests()
