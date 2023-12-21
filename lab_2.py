def embed_message(container_file, message):
    with open(container_file, 'rb') as file:
        header = file.read(138)
        container_data = [val for val in file.read()]

    # Преобразуем сообщение в двоичный вид
    binary_message = ''.join(format(ord(char), '016b') for char in message)

    # Вставляем сообщение в контейнер
    bit_count = 0
    for i in range(len(binary_message)):
        temp = container_data[i]
        temp = temp - temp % 2
        if binary_message[i] == '1':
            temp = temp + 1
        container_data[i] = temp
        bit_count += 1
    for i in range(len(binary_message), len(container_data)):
        container_data[i] = container_data[i] - container_data[i] % 2


    # Сохраняем информацию о количестве вставленных бит
    # можно использовать любой удобный способ для этого
    container_file = 'image+.bmp'

    with open(container_file, 'wb') as file:
        file.write(header)
        file.write(bytes(container_data))

    print("Сообщение успешно внедрено в контейнер.")
    print("Количество вставленных бит:", bit_count)


def extract_message(container_file):
    with open(container_file, 'rb') as file:
        header = file.read(138)
        container_data = [val for val in file.read()]


    binary_message = ''
    for i in range(len(container_data)):
        if container_data[i] % 2 == 0:
            binary_message += '0'
        else:
            binary_message += '1'

    message = ''
    zero_count = 0
    for i in range(0, len(binary_message), 16):
        byte = binary_message[i:i + 16]
        message += chr(int(byte, 2))
        if binary_message[i] == '0':
            zero_count += 1
        else:
            zero_count = 0
        if zero_count == 48:
            break

    print("Извлеченное сообщение:", message)

    return message


# Пример использования программы
container_file = 'image.bmp'
message = 'Секретное сообщение'

# Внедряем сообщение в контейнер
embed_message(container_file, message)
container_file = 'image+.bmp'

# Извлекаем сообщение из контейнера
extracted_message = extract_message(container_file)
print("Извлеченное сообщение:", extracted_message)
