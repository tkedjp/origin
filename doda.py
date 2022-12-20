from time import sleep

import requests
from bs4 import BeautifulSoup
import pandas as pd

company_list = []
base_url = 'https://doda.jp/DodaFront/View/JobSearchList.action?pr=13&pic=1&ds=0&oc=0112M%2C0113M%2C010401S%2C010402S%2C010404S&so=50&preBtn=1&pf=0&tp=1&page={}'

#長いので3ページ目まで取得
for i in range(3):
    url = base_url.format(i+1)

    sleep(3)

    r = requests.get(url, timeout=3)
    # r.raise_for_status()
    if r.status_code >= 300:
        print(F'{url}は無効です')
        continue

    soup = BeautifulSoup(r.content, 'lxml')
    page_urls = soup.select('.btnJob03')

    # print(page_urls)

    for page_url in page_urls:
        page_url = page_url.get('href')
        page_url = page_url.replace('_pr/', '_jd/')

        sleep(3)

        # print(page_url)

        page_r = requests.get(page_url, timeout=3)
        if page_r.status_code >= 300:
            print(F'{page_r}は無効です')
            continue

        page_soup = BeautifulSoup(page_r.content, 'lxml')

        company_name = page_soup.select_one('.job_title').text
        company_url_tag = page_soup.select_one('#company_profile_table > tbody > tr:last-of-type > td > a')
        company_url = company_url_tag.get('href') if company_url_tag else None

        # print(company_name)
        # print(company_url)

        print('='*30, i+1, '='*30)
        company_list.append({
            'company_name': company_name,
            'company_url': company_url
        })
        print(company_list[-1])

df = pd.DataFrame(company_list)
df.to_csv('company_list.csv', index=None, encoding='utf-8-sig')