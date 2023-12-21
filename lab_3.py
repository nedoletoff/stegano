from PIL import Image


def cox_algorithm_embed(image_path, secret_message, alpha):
    img = Image.open(image_path)
    pixels = img.load()

    width, height = img.size

    binary_secret_message = ''.join(format(ord(char), '08b') for char in secret_message)

    index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if index < len(binary_secret_message):
                r = int(format(r, '08b')[:-1] + binary_secret_message[index], 2)
                index += 1
            if index < len(binary_secret_message):
                g = int(format(g, '08b')[:-1] + binary_secret_message[index], 2)
                index += 1
            if index < len(binary_secret_message):
                b = int(format(b, '08b')[:-1] + binary_secret_message[index], 2)
                index += 1
            pixels[x, y] = (r, g, b)

    img.save('embedded_image.bmp')


# Пример использования функции
cox_algorithm_embed('image.bmp', 'Секретное сообщение0000000', 10)


def cox_algorithm_extract(image_path, message_length, alpha):
    img = Image.open(image_path)
    pixels = img.load()

    width, height = img.size
    binary_secret_message = ''

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_secret_message += format(r, '08b')[-1]
            binary_secret_message += format(g, '08b')[-1]
            binary_secret_message += format(b, '08b')[-1]

    secret_message = ''
    for i in range(0, message_length * 8, 8):
        byte = binary_secret_message[i:i + 8]
        secret_message += chr(int(byte, 2))

    return secret_message


# Пример использования функции
extracted_message = cox_algorithm_extract('embedded_image.bmp', len('Секретное сообщение'), 10)
print(extracted_message)
