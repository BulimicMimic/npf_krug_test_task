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


def check_time_interval(start, end, row):
    """
    Проверяем, входит ли запись в заданный временной диапазон.
    """
    time = get_time(row)
    return start <= time <= end


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
        header_row = next(reader)

        with open(output_path, 'w', encoding='cp1251') as output_file:
            writer = csv.writer(output_file, delimiter=';')
            writer.writerow(header_row)

            prev_row = next(reader)
            first_row = prev_row

            for row in reader:
                if (check_time_interval(start_time, end_time, row)
                        and check_aperture(aperture, row, prev_row)):
                    writer.writerow(row)
                prev_row = row

            # Проверка и запись в файл первой строки.
            if (check_time_interval(start_time, end_time, first_row)
                    and get_time(first_row) > get_time(row)):
                writer.writerow(first_row)


if __name__ == '__main__':
    aggregate_with_aperture(START, END, APERTURE, INPUT, OUTPUT)
