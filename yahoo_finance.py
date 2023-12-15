from time import sleep

import requests
from bs4 import BeautifulSoup
import pandas as pd

list = []

base_url = 'https://finance.yahoo.co.jp/stocks/ranking/marketCapitalLow?market=all&term=daily&page={}'

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
header = {
    'User-Agent': user_agent
}

sleep(3)

r = requests.get(base_url, timeout=7.5, headers=header)
if r.status_code >= 400:
    print(F'{base_url}は無効です')
soup = BeautifulSoup(r.content, 'lxml')

max_page_index = 10

for i in range(max_page_index):
    url = base_url.format(i+1)
    print(f'{i+1}ページ目URL:{url}')
    
    sleep(3)

    page_r = requests.get(url, timeout=7.5, headers=header)
    if page_r.status_code >= 400:
        print(F'{url}は無効です')
        continue

    page_soup = BeautifulSoup(page_r.content, 'lxml')

    table_soup = page_soup.select('div.XuqDlHPN tr._1GwpkGwB > td a')

    for table in table_soup:
        page_url_tag = table.get('href')

        if 'quote' in page_url_tag:
            page_url = page_url_tag

            company_r = requests.get(page_url, timeout=7.5, headers=header)
            if company_r.status_code >= 400:
                print(F'{url}は無効です')
                continue

            company_soup = BeautifulSoup(company_r.content, 'lxml')

            eps_tag = company_soup.select('#referenc > div ul li:nth-of-type(7) span._3rXWJKZF')

            for eps_number in eps_tag:
                eps_number = eps_number.text

                if '---' in eps_number:
                    eps = float(eps_number.replace('---', '0'))
                elif ',' in eps_number:
                    eps = float(eps_number.replace(',', ''))
                else:
                    eps = float(eps_number)

                if eps > 0:
                    bps_tag = company_soup.select('#referenc > div ul li:nth-of-type(8) span._3rXWJKZF')
                    
                    for bps_number in bps_tag:
                        bps_number = bps_number.text

                        if '---' in bps_number:
                            bps = float(bps_number.replace('---', '0'))
                        elif ',' in bps_number:
                            bps = float(bps_number.replace(',', ''))
                        else:
                            bps = float(bps_number)

                        if bps > 100:
                            company_name = company_soup.select_one('section._1zZriTjI._2l2sDX5w > div._1nb3c4wQ > header > div.DL5lxuTC > h2').text
                            stock_code = company_soup.select_one('section._1zZriTjI._2l2sDX5w > div._1nb3c4wQ div._23Y7QX2K > div._23Jev3qx span._2wsoPtI7').text                         
                            company_eps = eps
                            company_bps = bps

                            list.append({
                                '会社名': company_name,
                                '証券コード': stock_code,
                                'EPS': company_eps,
                                'BPS': company_bps
                            })
                            print(list[-1])

                else:
                    continue    
                
#Excel出力
df = pd.DataFrame(list)
df.to_excel('list.xlsx', index=False, encoding='utf-8-sig')