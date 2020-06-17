# v 0.32
import datetime
import time
from itertools import islice
import sqlite3
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(executable_path="C:\\Users\\Flare\\PycharmProjects\\scanner\\chromedriver.exe")

url = 'https://coinmarketcap.com/gainers-losers/'

p1 = '/html/body/div/div/div[2]/div[1]/div[2]/div[3]/ul[2]/li[1]/div/div[3]/div/table/tbody/tr['
p2 = ']'
p3 = '/td['
p4 = ']'
p5 = '/div/a'

exchange_1 = 'cmc-table > div:nth-child(3) > div > table > tbody > tr:nth-child('
exchange_2 = ')'
ex_1 = '>td:nth-child('
ex_2 = ')>div>a'

quantity = 5  # количество записей из топ списка
item = []
nested = []


def exchange(k):
    # вывод селекторов из таблицы для теста
    # print("{}{}{}{}{}{}".format(exchange_1, str(1), exchange_2, ex_1, str(k), ex_2))
    return exchange_1 + str(1) + exchange_2 + ex_1 + str(k) + ex_2


def init():
    driver.get(url)
    nested.clear()  # очистили внутренний список
    driver.execute_script("window.scrollTo(0, 1500)")
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/div[3]/ul[1]/li[1]').click()


def get_links():
    children = [a.get_attribute("href") for a in driver.find_elements_by_xpath(
        '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[3]/ul[2]/li[1]/div/div[3]/div/table/tbody/tr//div/a[@href]')]
    # Собираем только первые столбцы для перехода по монетам
    # Фильтруем ссылки до нужного количества
    for record in islice(children, quantity):
        driver.get(record)
        inner()


def inner():

    driver.execute_script("window.scrollTo(0, 1000)")
    time.sleep(5)
    driver.find_element_by_class_name('cmc-tabs__header > li:nth-child(2)').click()
    #driver.find_element_by_class_name('cmc-table__cell--sort-by__exchange-name > div > a').click()

    for i in range(1):
        nested.append([])
        if driver.find_elements_by_xpath(".//span[text() = 'Coin']"):
            nested[i - 1].append('Coin')
        else:
            nested[i - 1].append('Not Coin')
        for k in range(2, 4):  # количество ячеек
            path = exchange(k)
            href = driver.find_element_by_class_name(path).get_attribute('href')
            href_text = driver.find_element_by_class_name(path).text
            nested[i - 1].append({'href': href, 'href_text': href_text})

        nested[i - 1].append(datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"))


def open_browser():

    init()
    item.clear()
    print('массив очищен')

    for i in range(1, quantity + 1):
        item.append([])
        for k in range(2, 7):
            if k == 2:
                stale_el = driver.find_element_by_xpath(
                    '/html/body/div/div/div[2]/div[1]/div[2]/div[3]/ul[2]/li[1]/div/div[3]/div/table/tbody/tr[' +
                    str(i) + ']' + '/td[' + str(k) + ']//div/a')
                href = stale_el.get_attribute('href')
                href_text = stale_el.text
                item[i - 1].append({'href': href, 'href_text': href_text})
            else:
                stale = driver.find_element_by_xpath(
                    '/html/body/div/div/div[2]/div[1]/div[2]/div[3]/ul[2]/li[1]/div/div[3]/div/table/tbody/tr[' +
                    str(i) + ']' + '/td[' + str(k) + ']').text
                driver.implicitly_wait(5)
                item[i - 1].append(stale)

    get_links()  # получили внутренний список
    print("внутренний список получен")
    res = list(zip(item, nested))
    print("склеили списки")
    create_db(res)


def create_db(res):
    conn = sqlite3.connect("coins1.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS setcoins (name TEXT, symbol TEXT, volume24h TEXT, price TEXT, diff TEXT, type TEXT, exchange TEXT, link TEXT, date TEXT)")  # 10
    elem = []

    for i in range(len(res)):
        elem.append([])
        for y in range(len(res[i])):
            for z in range(len(res[i][y])):
                if isinstance(res[i][y][z], dict):
                    elem[i].append(res[i][y][z].get('href_text'))
                else:
                    elem[i].append(res[i][y][z])

        cursor.execute('''INSERT INTO setcoins VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''', elem[i])

    conn.commit()
    print('завершена запись в базу')
    elem.clear()
    print('очистили элементы строки')

    n = cursor.execute("SELECT COUNT(*) FROM setcoins")
    values = n.fetchone()
    print('текущее количество строк в базе: ', values[0])


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
            if row is None or iter == value2[0]:
                break
            my_list.insert(iter, [row[0], round(row[1] * 100 / s_100, 5), row[1]])
            iter += 1

    return sorted(my_list, key=lambda k: k[1], reverse=True)

