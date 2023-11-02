import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver

options = webdriver.ChromeOptions()
# options.add_argument('--incognito')
# options.add_argument('--headless')

driver = webdriver.Chrome(
    executable_path='/Users/takashie/Desktop/Lesson/hayatasu/section08/tools/chromedriver',
    options=options)
driver.implicitly_wait(10)

# max_page_index = 188

base_url = 'https://www.athome.co.jp/estate/osaka/list/?pref=27'

driver.get(base_url)
sleep(3)

page_links = driver.find_elements_by_css_selector(
    '.card-box__area')
print(page_links)
links = [page_link.get_attribute('href') for page_link in page_links]
print(links)

#pythonファイルのあるディレクトリパス取得
dir_path = os.path.dirname(os.path.abspath(__file__))

for i, link in enumerate(links):
    print('='*30, i, '='*30)
    print(link)
    driver.get(link)
    sleep(5)

    html = driver.page_source

    #dir_pathの中のhtmlというフォルダに，ファイル名{driver.title}.htmlで保存できる
    p = os.path.join(dir_path, 'html', f'{driver.title}.html')
    with open(p, 'w') as f:
        f.write(html)

sleep(3)
driver.quit()