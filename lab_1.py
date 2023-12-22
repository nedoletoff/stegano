def embed_message(container_file, message):
    with open(container_file, 'r', encoding='utf-8') as file:
        container_text = file.read()

    # Преобразуем сообщение в двоичный вид
    binary_message = ''.join(format(ord(char), '016b') for char in message)

    # Вставляем сообщение в контейнер
    container_list = list(container_text)
    bit_count = 0
    for i in range(len(container_list)):
        if container_list[i] == ' ':
            if bit_count < len(binary_message):
                container_list[i] = '\u00A0' if binary_message[bit_count] == '1' else ' '
                bit_count += 1
            else:
                break

    # Сохраняем информацию о количестве вставленных бит
    # можно использовать любой удобный способ для этого
    container_file = 'container+.txt'

    with open(container_file, 'w', encoding='utf-8') as file:
        file.write(''.join(container_list))

    print("Сообщение успешно внедрено в контейнер.")
    print("Количество вставленных бит:", bit_count)


def extract_message(container_file):
    with open(container_file, 'r', encoding='utf-8') as file:
        container_text = file.read()

    # Извлекаем сообщение из контейнера
    binary_message = ''
    counter = 0
    for char in container_text:
        counter+=1
        if char == '\u00A0':
            binary_message += '1'
        elif char == ' ':
            binary_message += '0'

    message = ''
    for i in range(0, len(binary_message), 16):
        byte = binary_message[i:i + 16]
        message += chr(int(byte, 2))
    print(f'capacity {counter}')

    return message


# Пример использования программы
container_file = 'container.txt'
message = 'Секретное сообщение'

# Внедряем сообщение в контейнер
embed_message(container_file, message)

container_file = 'container+.txt'

# Извлекаем сообщение из контейнера
extracted_message = extract_message(container_file)
print("Извлеченное сообщение:", extracted_message)