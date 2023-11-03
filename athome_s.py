import re
import os
from glob import glob

from bs4 import BeautifulSoup
import pandas as pd

html_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'html', '*')

# print(html_path)

list = []
for path in glob(html_path):
    with open(path, 'r') as f:
        html = f.read()

    f_name = os.path.basename(path)
    soup = BeautifulSoup(html, 'lxml')

    company_name = soup.select_one('.est_h1_name').text
    address = soup.select_one('.table-address p').text
    address = address.replace('\n','')
    address = address.strip()
    tel_fax = soup.select_one('.table-tel p').text
    tel_fax= tel_fax.replace('\n','')
    tel_fax = tel_fax.strip()

    licence_number = soup.select_one('td:-soup-contains("免許")').text
    site_url_tag = soup.select_one('a:-soup-contains("ホームページ")')
    if site_url_tag is None:
        site_url = '-'
    else:
        site_url = site_url_tag.get('href')

    list.append({
        '会社名': company_name,
        '住所': address,
        'TEL/FAX': tel_fax,
        '免許番号': licence_number,
        'ホームページ': site_url,
        })
    print(list[-1])

#csv出力
df = pd.DataFrame(list)
df.to_csv('list.csv', index=False, encoding='utf-8-sig')