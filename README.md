# testExerciseINITI
## Задание
Существует условный сервер, на котором в оперативной памяти хранится очень длинная таблица (миллионы строк).
Строки отсортированы в некотором порядке, принцип сортировки может меняться, каждая строка имеет свой уникальный идентификатор.
Таблица живая, постоянно изменяется (несколько сотен/десятков изменений в секунду). В нее добавляются новые строки, обновляются и удаляются существующие.

Кроме этого, существует условный клиент, задача которого - отображение этой таблицы в реальном времени (все изменения видны сразу). При этом памяти на клиенте недостаточно для выгрузки всей таблицы.
Отображение осуществляется за счет того, что пользователю доступно окно высотой в N строк и в нём скроллер, позволяющий передвигаться по списку и сортировать ее по столбцам. При этом пользователь не ограничен в своих действиях - он может скроллироваться в любую часть списка и выбирать любой столбец для сортировки. Например, если на сервере список из миллиона записей и на клиенте скроллер передвинут на середину, то клиент должен отобразить N записей начиная с полумллионной.

Задача - придумать способ для хранения таблицы на сервере и протокол взаимодействия клиента и сервера для быстрого и корректного отображения данных клиентами. Важно, чтобы решение не предполагало использование сторонних продуктов (например, СУБД) или фреймворков. Следует использовать базовые контейнеры данных для выбранного для решения задачи языка (например, контейнеры стандартной библиотеки STL в случае реализации на C++ - map, vector, list или их аналоги в других языках).
В идеале - создать прототип на любом языке программирования, но вполне достаточно четко описать предполагаемую реализацию.
## Решение
### Способ хранения данных
Так как от контейнера требуется возможность добавления/изменения/удаления строк, я выбрал двумерный массив. Подмассивы в данном случае олицетворяют собой строку в таблице, то есть имеют одинаковое количество элементов. Идентификатором подмассива выступает идентификатор внутри основного массива, так он автоматически изменяется при добавлении или удалении элементов.
### Сортировка
Так как пользователь видит ограниченное число строк, а набор данных постоянно меняется, я сделал сортировку в серверном приложении. Устроена она следующим образом:
1. Берется колонка и формируется промежуточный двумерный массив из подмассивов.
2. В каждом из подмассивов 2 элемента: id в изначальном массиве и значение из колонки.
3. Происходит сортировка по выделенному значению (то есть по колонке).
4. Сохраняется одномерный массив из id элементов изначального массива.
5. Таким образом формируется сортировочный двумерный массив. Каждый элемент этого массива -- подмассив, содержащий id подмассивов (строк) изначального массива.
```
[[3, ...],  -> [[1, 3],  -> [[2, 1],  -> [2,
 [1, ...],      [2, 1],      [3, 2],      3,      
 [2, ...],      [3, 2],      [1, 3],      1,      
 ...            ...          ...          ...          
]              ]            ]            ]
```
### Серверное приложение
Серверное приложение написано на Python с использованием FastAPI. Есть методы получения/добавления/изменения/удаления данных в контейнере хранения.
### Клиентсоке приложение
Клиентское приложение написано с использованием PySide6. Окно содержит таблицу и кнопку, нажатие которой запускает автообновление таблицы. Полосы прокрутки нет, прокручивать строки можно с помощью колесика мыши.
#### Клиент-серверное взаимодействие
После запуска или после нажатия кнопки клиентское приложение (единожды или многократно и непрерывно, соответственно) шлет запрос на сервер. Этот запрос всегда содержит: 
1. Номер строки, с которой нужно выделить данные (изменяется при прокрутке колесиком).
2. Количество строк, которые нужно вырнуть в ответе (изменяется в коде).
3. Колонку, по которой сейчас активна сортировка (изменяется при нажатии на колоку таблицы).
4. Булевой значение, которое показывает, прямая ли сортировка или обратная (изменяется при ПОВТОРНОМ нажатии на колоку таблицы).
По полученному запросу сервер:
1. Выбирает сортировочный массив
2. Инверсирует его, если сортировка обратная
3. Выделяет, с какого по какой элемент сортировочного массива вернуть клиенту.
4. Заменяет эти элементы по принципу изначальный массив[элемент соритровочного массива] = элемент изначального массива и формирует из них массив для отправки клиенту.
5. Получившийся двумерный массив возвращается клиенту и сразу отображается, так как уже находится в нужном формате.
### Тестовый набор данных
Для теста был сформирован набор из 1 000 000 строк. В каждой строке -- 6 колонок:
1. id
2. Name
3. Age
4. Heights
5. Foot
6. Englist.
#### id -- не id
Колонку id я сделал исключительно для демонстрации отображения изменений у клиента в реальном времени. В логике работы приложения она никак не учавствует.
### Немного циферок
1. Сортировка одной колонки из 1 000 000 строк происходит за 1.4 секунды.
2. Получение кортежа от сервера для 10 строк (для такого количества строк сейчас сделано приложение) занимает 0.08 мс. Для 100 строк -- уже 1.4 секунды.
### Запуск приложений
1. Клонировать репо
2. Установка virtualenv
```
pip3 install virtualenv
```
3. Создание виртуального окружения
```
python3 -m venv test
```
4. Установка библиотек
```
. test\bin\activate && pip install -r requirements.txt
```
#### Сервер
```
test\bin\python .\server\main.py --port 80 --data_path ".\server\data.csv"
```
#### Клиент
```
test\bin\python .\client\main.py
```
