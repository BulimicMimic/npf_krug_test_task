import csv
import time
from datetime import datetime

INPUT = '786442_Ribbon1 Сводная.csv'
OUTPUT = '786442_Ribbon1 Выборочная.csv'
APERTURE = 1
START = '7:58:10.002'
END = '9:58:52.002'
# START = '7:58:40.022'
# END = '9:58:52.002'


def execution_time(func):
    """
    Функция-декоратор для подсчета времени выполнения функции-аргумента.
    """
    def wrapper(*args):
        start_time = time.time()
        result = func(*args)
        execution_time = round(time.time() - start_time, 10)
        print(f'Время выполнения функции: {execution_time} с.')
        return result
    return wrapper


def get_time(row):
    """
    Получаем время из строки данных
    """
    _, _, _, _, time, _ = row[1].split()
    time = datetime.strptime(time, '%H:%M:%S.%f')
    return time


def broken_search(rows, target):
    """
    Функция бинарного поиска в массиве со смещенными данными,
    где запись значений ведется циклически. При достижении конца массива
    новые данные записываются в начало массива.
    Используется для поиска индекса начала и конца временного диапазона.
    """
    left = 0
    right = len(rows) - 1
    if get_time(rows[right]) < target < get_time(rows[left]):
        return right
    mid = left + (right - left) // 2
    while left != mid:
        if get_time(rows[mid]) == target:
            return mid
        elif get_time(rows[mid]) > get_time(rows[right]):
            if get_time(rows[left]) <= target < get_time(rows[mid]):
                right = mid
            else:
                left = mid
        elif get_time(rows[mid]) < get_time(rows[right]):
            if get_time(rows[mid]) < target <= get_time(rows[right]):
                left = mid
            else:
                right = mid
        mid = left + (right - left) // 2
    return mid


def check_aperture(aperture, row, row_prev):
    """
    Проверяем, отличается ли хотя бы один параметр записи от аналогичного
    параметра предыдущей записи на значение, большее заданной апертуры.
    """
    for idx in range(2, len(row)):
        if abs(float(row[idx].replace(',', '.'))
               - float(row_prev[idx].replace(',', '.'))) > aperture:
            return True
    return False


@execution_time
def aggregate_with_aperture(
        start_time, end_time, aperture, input_path, output_path):
    """
    Основная функция.
    Здесь считывается файл с данными.
    Данные, подходящие под критерии записываются в файл вывода.
    """
    start_time = datetime.strptime(start_time, '%H:%M:%S.%f')
    end_time = datetime.strptime(end_time, '%H:%M:%S.%f')

    with open(input_path, 'r', encoding='cp1251') as input_file:
        reader = csv.reader(input_file, delimiter=';')
        rows = list(reader)
        header_row = rows.pop(0)

        start_idx = broken_search(rows, start_time)
        end_idx = broken_search(rows, end_time)

        with open(output_path, 'w', encoding='cp1251') as output_file:
            writer = csv.writer(output_file, delimiter=';')
            writer.writerow(header_row)

            # Проверятеся пересекает ли временной диапазон конец файла данных.
            # В зависимости от этого выбирается алгоритм обработки.
            if start_idx > end_idx:
                for idx in range(0, end_idx + 1):
                    if check_aperture(aperture, rows[idx], rows[idx - 1]):
                        writer.writerow(rows[idx])

                for idx in range(start_idx, len(rows)):
                    if check_aperture(aperture, rows[idx], rows[idx - 1]):
                        writer.writerow(rows[idx])

            else:
                if start_idx == 0:
                    start_idx += 1
                    if (get_time(rows[0]) > get_time(rows[-1])
                            and check_aperture(aperture, rows[0], rows[-1])):
                        writer.writerow(rows[0])

                for idx in range(start_idx, end_idx+1):
                    if check_aperture(aperture, rows[idx], rows[idx-1]):
                        writer.writerow(rows[idx])


if __name__ == '__main__':
    aggregate_with_aperture(START, END, APERTURE, INPUT, OUTPUT)
