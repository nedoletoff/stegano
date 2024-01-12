from Crypto.Cipher import AES

p = 13
gen = [2, 6, 11, 7]
block_size = 16
extra = ' '


def pad(s):
    return s + (block_size - len(s) % block_size) * extra


def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    return cipher.encrypt(pad(message))


def decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    return cipher.decrypt(ciphertext)


