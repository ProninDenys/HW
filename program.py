import re

# Имя файла
file_name = 'regex_sum_2133029.txt'

try:
    # Открываем файл и читаем его содержимое
    with open(file_name, 'r') as file:
        data = file.read()
    
    # Находим все числа в файле с помощью регулярного выражения
    numbers = re.findall(r'[0-9]+', data)
    
    # Преобразуем найденные числа в целые и вычисляем их сумму
    total_sum = sum(int(num) for num in numbers)
    
    print("Сумма чисел:", total_sum)
except FileNotFoundError:
    print(f"Файл '{file_name}'")
