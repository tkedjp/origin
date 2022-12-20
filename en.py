from time import sleep

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://employment.en-japan.com/search/search_list/?areaid=23&occupation=100000&aroute=1&pagenum={}'

#長いので3ページ目まで取得
max_page_index = 3
en_list = []

for i in range(max_page_index):
    access_url = url.format(i+1)

    sleep(3)
        
    r = requests.get(access_url, timeout=3)
    if r.status_code >= 300:
        print(F'{url}は無効です')
        continue

    soup = BeautifulSoup(r.content, 'lxml')
    page_urls = soup.select('.buttonArea > a:last-of-type')

    for page_url in page_urls:
        access_url = 'https://employment.en-japan.com' + page_url.get('href')

        sleep(3)

        page_r = requests.get(access_url, timeout=3)
        if page_r.status_code >= 300:
            print(F'{access_url}は無効です')
            continue
        page_soup = BeautifulSoup(page_r.content, 'lxml')

        if 'fromSearch' not in access_url:
            company_name = page_soup.select_one('h2:-soup-contains("会社概要") > span').text
            company_tag = page_soup.select_one('a.previewOption')
            company_url = company_tag.get('href') if company_tag else None

        else:
            detail_page_url = page_soup.select_one('#recruitFrame').get('src')

            sleep(3)

            detail_page_r = requests.get(detail_page_url, timeout=3)
            if detail_page_r.status_code >= 300:
                print(F'{detail_page_url}は無効です')
                continue
            detail_page_soup = BeautifulSoup(detail_page_r.content, 'lxml')

            company_name = detail_page_soup.select_one('.companyTable > tbody > tr > td').text
            company_url_tag = detail_page_soup.select_one(
                '.companyTable > tbody > tr:nth-of-type(3) td > a')
            company_url = company_url_tag.get('href') if company_url_tag else None
         
        print('='*70)
        print(company_name)
        print(company_url)

        en_list.append({
        'company_name': company_name,
        'company_url': company_url
        })
        print(en_list[-1])

df = pd.DataFrame(en_list)
df.to_csv('enjapan_company_list.csv', index=False, encoding='utf-8-sig')