from time import sleep

import requests
from bs4 import BeautifulSoup
import pandas as pd

max_page_index = 5
company_list = []

base_url = 'https://next.rikunabi.com/miyagi/jb0500000000/crn{}.html'

for i in range(max_page_index):
    print('company_list:', len(company_list))
    url = base_url.format(1+50*i)

    sleep(3)
    
    r = requests.get(url, timeout=3)
    if r.status_code >= 300:
        print(F'{url}は無効です')
        continue

    soup = BeautifulSoup(r.content, 'lxml')
    page_urls = soup.select('.rnn-textLl > a')

    for i, page_url in enumerate(page_urls):
        page_url = 'https://next.rikunabi.com' + page_url.get('href')

        sleep(3)

        page_r = requests.get(page_url, timeout=3)
        if page_r.status_code >= 300:
            print(F'{page_url}は無効です')
            continue

        page_soup = BeautifulSoup(page_r.content, 'lxml')

        if 'company' in page_url:
            company_page_urls = page_soup.select('a:-soup-contains("企業ページ")')
            for company_page_url in company_page_urls:
                company_page_url = 'https://next.rikunabi.com' + company_page_url.get('href')

                sleep(3)

                company_page_r = requests.get(company_page_url, timeout=3)
                if company_page_r.status_code >= 400:
                    print(F'{company_page_url}は無効です')
                    continue

                company_page_soup = BeautifulSoup(company_page_r.content, 'lxml')

                company_name = company_page_soup.select_one(
                '.rnn-breadcrumb > li:last-of-type').text

                url_in_tag = company_page_soup.select_one('.rnn-col-11:last-of-type a')
                company_url = url_in_tag.get('href') if url_in_tag else None

        else:
            company_name = page_soup.select_one('p:nth-of-type(2)').text
            company_url = None

        print('='*70)
        print(company_name)
        print(company_url)
        
        company_list.append({
        'company_name': company_name,
        'company_url': company_url
        })
        print(company_list[-1])

df = pd.DataFrame(company_list)
df.to_csv('company_list.csv', index=None, encoding='utf-8-sig')