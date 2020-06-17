import sqlite3


def sorting_list():
    s_100 = 0
    my_list = []
    conn = sqlite3.connect("coins1.db")
    cursor = conn.cursor()
    n = cursor.execute("SELECT COUNT(*) FROM setcoins")
    value1 = n.fetchone()
    print('-----------------------------------------------')
    print('Всего строк в базе: ', value1[0])
    n2 = cursor.execute("SELECT COUNT(DISTINCT exchange) FROM setcoins")
    value2 = n2.fetchone()
    print('Количество уникальных бирж без дублей: ', value2[0])
    print('-----------------------------------------------')

    # подсчет текущей суммы уникальных бирж
    with conn:
        x = conn.execute("SELECT exchange, COUNT(DISTINCT name) AS qty FROM setcoins GROUP BY exchange")
        while True:
            row = x.fetchone()
            if row is None:
                break
            s_100 += row[1]

    # расчет процентов
    with conn:
        x = conn.execute("SELECT exchange, COUNT(DISTINCT name) AS qty FROM setcoins GROUP BY exchange")
        iter = 0
        while True:
            row = x.fetchone()
            if row is None:
                break
            my_list.insert(iter, [row[0], round(row[1] * 100 / s_100, 5), row[1]])
            iter += 1

    return sorted(my_list, key=lambda k: k[1], reverse=True)


s_list = sorting_list()
c = len(s_list)

i = 0
while i < c:
    print(s_list[i][0], s_list[i][1], '%', '[' + str(s_list[i][2]) + ']')
    i += 1
