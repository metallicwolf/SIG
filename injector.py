import mysql.connector

"""
Мой временный крипт для загрузки большого количества данных в таблицу. Через терминал не получается
загрузить примерно больше 100 запросов. Формат исходного файла такой:

Первая строка не содержит комментарий, а сразу запрос.
Дальнейшие маркеры это /* INSERT QUERY NO: 2 */

Запросы генерировал на сайте https://wtools.io/ru/convert-csv-to-sql-queries. Копировал их в файл 1.sql.

"""

filename = '/home/vi/1.sql'
DB_NAME = 'w2_lab'
cnx = mysql.connector.connect(user='root', password='Ovill@1930', host='127.0.0.1')
cursor = cnx.cursor()

cursor.execute("USE {}".format(DB_NAME))

with open(filename, newline='') as File:
    line = ""
    for row in File:
        current_row = row[:30]

        if 'INSERT QUERY' not in current_row:
            line = line + row
        elif 'INSERT QUERY' in current_row:
            # if line[-1] != ';':
            #     line += ';'
            print(line)
            cursor.execute(line)
            line = ""

cnx.commit()
cursor.close()
cnx.close()