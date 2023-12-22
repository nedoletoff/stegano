import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack.dct
import scipy.fftpack.idct


def dct2(a):
    """Выполняет 2D дискретное косинусное преобразование для матрицы a.

  Args:
    a: Матрица входных данных.

  Возвращает:
    Матрица выходных данных.
  """

    m, n, _ = a.shape
    # Создаем матрицу коэффициентов DCT.
    c = np.zeros((m, n), dtype=complex)
    for u in range(m):
        for v in range(n):
            for i in range(m):
                for j in range(n):
                    c[u, v] += a[i, j] * np.cos((2 * np.pi * (i * u + j * v)) / (m * n))
    # Нормируем матрицу коэффициентов DCT.
    c /= np.sqrt(m * n)
    return c


def idct2(c):
    """Выполняет обратное 2D дискретное косинусное преобразование для матрицы c.

  Args:
    c: Матрица входных данных.

  Возвращает:
    Матрица выходных данных.
  """

    m, n = c.shape
    # Создаем матрицу коэффициентов IDCT.
    a = np.zeros((m, n), dtype=complex)
    for u in range(m):
        for v in range(n):
            for i in range(m):
                for j in range(n):
                    a[i, j] += c[u, v] * np.cos((2 * np.pi * (i * u + j * v)) / (m * n))
    # Нормируем матрицу коэффициентов IDCT.
    a /= np.sqrt(m * n)
    return a


def dct_color(image):
    """Выполняет DCT для цветного изображения.

  Args:
    image: Цветное изображение в виде массива NumPy.

  Возвращает:
    Матрица коэффициентов DCT для каждого канала.
  """

    # Разделяем изображение на каналы.
    channels = np.split(image, 3, axis=2)
    # Вычисляем DCT для каждого канала.
    dct_channels = [dct(channel) for channel in channels]
    # Возвращаем матрицы коэффициентов DCT.
    return dct_channels


def idct_color(dct_channels):
    """Выполняет обратное DCT для цветного изображения.

  Args:
    dct_channels: Матрица коэффициентов DCT для каждого канала.

  Возвращает:
    Цветное изображение в виде массива NumPy.
  """

    # Объединяем каналы.
    channels = [idct(channel) for channel in dct_channels]
    channels = np.stack(channels, axis=2)
    return channels


def embed_information(image, data, a, block_size=8):
    """Встраивает информацию в изображение алгоритмом Cox.

  Args:
    image: Цветное изображение в виде массива NumPy.
    data: Информация, которую необходимо встроить.
    a: Коэффициент внедрения.
    block_size: Размер блока DCT.

  Возвращает:
    Изображение с внедренной информацией.
  """

    # Вычисляем DCT для изображения.
    dct_channels = dct_color(image)

    # Находим индексы самых больших коэффициентов AC в каждом блоке.
    max_indices = []
    for channel in dct_channels:
        max_indices.append(np.argmax(channel, axis=1))

    # Вставляем информацию в коэффициенты AC.
    for channel, index, value in zip(dct_channels, max_indices, data):
        channel[index // block_size, index % block_size] = channel[index // block_size, index % block_size] * (
                1 + a * value)

    # Вычисляем обратное DCT для изображения.
    return idct_color(dct_channels)


def decode_image(filename):
    pass


def change_message(message):
    m = []
    for i in message:
        if i == 0:
            m.append(-1)
        else:
            m.append(1)

    return m


# Загружаем изображение.
image = plt.imread("lena.bmp")

# Генерируем данные для внедрения.
data = np.random.randint(0, 255, (3, 100))

# Встраиваем информацию в изображение.
embedded_image = embed_information(image, data, 0.1, block_size=8)

# Отображаем изображение до и после внедрения.
plt.subplot(121)
plt.imshow(image)
plt.title("Исходное изображение")
plt.subplot(122)
plt.imshow(embedded_image)
plt.title("Изображение с внедренной информацией")
plt.show()
