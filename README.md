## Тестовое задание НПФ «КРУГ»

### Автор: 
Алаткин Александр

### Описание:
Реализация тестового задания от работодателя НПФ «КРУГ».<br>
Тестовое задание Python
В таблицу базу данных (в данном случае приложенный csv файл) периодически записываются
значения параметров в вещественном формате:
&lt;Номер записи&gt;&lt;Дата и время записи&gt;&lt;Значение параметра 1&gt;&lt;Значение параметра 2&gt;…
Таблица имеет ограниченное количество записей. Запись значений ведется циклически. При
достижении конца таблицы новые данные записываются в начало таблицы.

Необходимо реализовать следующую функцию выборки данных:
В функцию передается время начала диапазона, время конца диапазона, апертура значений
параметров.
Из таблицы за заданный диапазон необходимо вернуть строки таблицы, в которых хотя бы один
параметр отличается от предыдущего на значение большее апертуры.

Результат – таблица в csv. Также вывести время выполнения функции.

### Реализация:
Выполнено два варианта реализации:
Первый в файле aggregator.py использует обычный перебор всего файла данных.
Второй создает список с данными и перебирает только данные из указанного временного интервала.
Индексы начала и конца временного интервала ищутся с помощью бинарного поиска.

Первый вариант выигрывает по времени, вероятно из-за того, что второй тратит много ресурсов на построение списка данных.
