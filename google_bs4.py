from time import sleep, time
from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
# options.add_argument('--headless')

# driver = webdriver.Chrome(
#     executable_path='/Users/takashie/Desktop/Lesson/hayatasu/section08/tools/chromedriver',
#     options=options)

driver = webdriver.Chrome(
    options=options)

driver.implicitly_wait(10)

driver.get('https://news.google.com/')
sleep(3)

search_box = driver.find_element_by_css_selector('input.Ax4B8')
sleep(3)

search_box.send_keys('機械学習' + Keys.ENTER)
sleep(3)

#検索キーワードを入力した後
height = driver.execute_script('return document.body.scrollHeight') # ここの初期値が最初1000なら
new_height = 0

while True:    
    # print(height)
    driver.execute_script(f'window.scrollTo(0, {height})') # ここで1000だけスクロールする
    sleep(5)    

    new_height = driver.execute_script('return document.body.scrollHeight') #2000    

    if height == new_height: #もし値が等しくなったらこのwhile文を抜ける        
        break

height = new_height

# start = time()

# #Selenium解析
# a_tags = driver.find_elements_by_css_selector('a.newsFeed_item_link')

# for i, a_tag in enumerate(a_tags):
#     print('='*30, i, '='*30)
#     print(a_tag.find_element_by_css_selector('.newsFeed_item_title').text)
#     print(a_tag.get_attribute('href'))

# print('='*30)
# print(time() - start)
# print('='*30)


# #BeautifulSoup解析
search_list = []
soup = BeautifulSoup(driver.page_source, 'lxml')
a_tags = soup.select('h3.ipQwMb')
sleep(3)

for i, a_tag in enumerate(a_tags):
    print('='*30, i, '='*30)
    title = a_tag.select_one('.DY5T1d').text
    page_url ='https://news.google.com/' + a_tag.select_one('.DY5T1d').get('href')
    page_url = page_url.replace('/.', '')
    print(title)
    print(page_url)

    search_list.append({
        'title': title,
        'page_url': page_url
    })
    print(search_list[-1])

# print('='*30)
# print(time() - start)
# print('='*30)

driver.quit()

df = pd.DataFrame(search_list)
df.to_csv('search_list.csv', index=None, encoding='utf-8-sig')