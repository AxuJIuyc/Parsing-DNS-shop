from gettext import install

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep
from tqdm import tqdm
from selenium.webdriver import Chrome
# from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By

browser = Chrome(r"C:\Users\Lao98\Desktop\Python\Parsing\chromedriver")
url = 'https://www.dns-shop.ru/'
urlVC = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/'
browser.get(urlVC)
sleep(3)

AnotherCity = browser.find_element(By.LINK_TEXT, 'Выбрать другой')
AnotherCity.click()
sleep(3)

City = browser.find_element(By.LINK_TEXT, 'Новосибирск')
City.click()
sleep(3)

data = []

for p in range(1, 12):
    bottom = browser.find_element(By.CLASS_NAME, 'pagination-widget__page-link_next ')
    soup = bs(browser.page_source, 'lxml')
    videocards = soup.find_all('div', class_='catalog-product')
    for i in videocards:
        try:
            link = url + i.find('a').get('href')
        except:
            link = 'null'
        try:
            name = i.find('span').text[11:]
        except:
            name = 'null'
        try:
            price = i.find('div', class_='product-buy__price').text
            price = price[:-1]
            price = price.replace(' ', '')
            int(price)    
        except:
            price = 'null'
        try:
            rating = i.find('a', class_='catalog-product__rating').get('data-rating')
            rating = rating.replace('.', ',')
        except:
            rating = 'null'
        try:
            available = i.find('span', class_='available').text[:-2]
        except:
            try:
                available = i.find('div', class_='order-avail-wrap order-avail-wrap_not-avail').text.strip()
            except:
                available = 'null'  
        data.append([available, price, name, rating, link])
    try:
        bottom.click()
        print(p,' next page')
    except:
        print(p, 'error')
    sleep(3)
data

header = ['available', 'price', 'name', 'rating', 'link']
table = pd.DataFrame(data, columns=header)
table.to_csv(r'C:\Users\Lao98\Desktop\Python\Parsing\pars_DNS-videocards.csv', sep=';', encoding='utf8')