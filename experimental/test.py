import math


def calculate_digit_coordinates(num_digits, distance):
    coordinates = []
    angle = 2 * math.pi / num_digits  # Вычисляем угол между каждой цифрой

    for i in range(num_digits):
        x = distance * math.cos(i * angle) * 5  # Вычисляем x-координату
        y = distance * math.sin(i * angle) * 5  # Вычисляем y-координату
        coordinates.append((x, y))

    return coordinates


# Пример использования функции
num_digits = 5
distance = 1
digit_coordinates = calculate_digit_coordinates(num_digits, distance)

# Вывод координат цифр
for i, coord in enumerate(digit_coordinates):
    print(f"Координаты цифры {i+1}: {coord}")


import matplotlib.pyplot as plt

# Разделение координат на отдельные списки для x и y
x_coords = [coord[0] for coord in digit_coordinates]
y_coords = [coord[1] for coord in digit_coordinates]

# Создание графика
plt.scatter(x_coords, y_coords)
plt.axis("equal")  # Сделать оси равными для правильного отображения
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Координаты цифр на циферблате")

# Показать график
plt.show()
