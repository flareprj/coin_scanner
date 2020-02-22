# v 0.1
import time
import numpy as np
from itertools import islice

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()

#options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome()

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

quantity = 15  # количество записей
item = []
nested = []


def arr1(p1, p2, p3, p4, i, k):
    return p1 + str(i) + p2 + p3 + str(k) + p4


def link1(p1, p2, p3, p4, p5, i, k):
    return p1 + str(i) + p2 + p3 + str(k) + p4 + p5


def exchange(k):
    return exchange_1 + str(1) + exchange_2 + ex_1 + str(k) + ex_2


def init():
    driver.get(url)
    #time.sleep(3)
    driver.execute_script("window.scrollTo(0, 1500)")
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/div[3]/ul[1]/li[1]').click()


def get_links():

    init()
    children = [a.get_attribute("href") for a in driver.find_elements_by_xpath(
        '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[3]/ul[2]/li[1]/div/div[3]/div/table/tbody/tr//div/a[@href]')]
    # Собираем только первые столбцы для перехода по монетам
    # Фильтруем ссылки до нужного количества
    for record in islice(children, quantity):
        driver.get(record)
        inner(nested)



def inner(nested):

    driver.execute_script("window.scrollTo(0, 1500)")
    #time.sleep(3)
    driver.find_element_by_class_name('cmc-tab__detail-market').click()
    driver.find_element_by_class_name('cmc-popover__dropdown > ul > li:nth-child(1)').click()

    for i in range(1):
        nested.append([])
        if driver.find_elements_by_xpath(".//span[text() = 'Coin']"):
            nested[i-1].append('Coin')
        else:
            nested[i-1].append('Not Coin')
        for k in range(2, 4):  # количество ячеек
            path = exchange(k)
            href = driver.find_element_by_class_name(path).get_attribute('href')
            href_text = driver.find_element_by_class_name(path).text
            nested[i - 1].append({'href': href, 'href_text': href_text})


def open_browser():

    init()
    start_time = time.time()

    for i in range(1, quantity + 1):
        item.append([])
        for k in range(1, 7):
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

    get_links()

    print("Время:", time.time() - start_time)

    return item, nested



