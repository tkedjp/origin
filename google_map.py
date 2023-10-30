from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

df = pd.read_excel('地図調査一覧.xlsx') 

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(
    executable_path='',
    options=options)
driver.get('https://www.google.co.jp/maps/')
time.sleep(3)

for i, r in df.iterrows():
    driver.find_element(By.ID, "searchboxinput").click()
    driver.find_element(By.ID, "searchboxinput").send_keys(r['地名'])
    driver.find_element(By.ID, "searchboxinput").send_keys(Keys.ENTER)
    time.sleep(2)
    df.loc[i,'住所'] = driver.find_element(By.CSS_SELECTOR, ".RcCsl:nth-child(3)").text
    print(df.loc[i,'住所'])
    df.loc[i,'電話'] = driver.find_element(By.CSS_SELECTOR, 'button > div > div.rogA2c').text
    print(df.loc[i,'電話'])
    if df.loc[i,'電話'] is None:
        df.loc[i,'電話'] = None
    else:
        continue
    driver.save_screenshot(r['地名']+'.png')
    driver.find_element(By.ID, "searchboxinput").clear()

df.to_excel('地図調査一覧.xlsx', index=None) 

time.sleep(5)
driver.quit()