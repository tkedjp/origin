import requests
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(
    executable_path='/Users/takashie/Desktop/Lesson/hayatasu/section08/tools/chromedriver',
    options=options)
driver.implicitly_wait(10)

driver.get('https://www.mizuhobank.co.jp/rate_fee/rate_interest.html')
sleep(3)

soup = BeautifulSoup(driver.page_source, 'lxml')
tables = soup.select_one('table.type1')
sleep(3)

for tr in tables.select('tr'):
    cell1, cell2 = tr.select('*')
    print(cell1.string.strip(), cell2.string.strip())

driver.quit()