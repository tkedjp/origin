from time import sleep
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

def normalize_spaces(s):
    """
    連続する空白を1つのスペースに置き換える re.sup() 前後の空白を削除した新しい文字列を取得　strip()
    """
    #re.sub()では第一引数に正規表現パターン、第二引数に置換先文字列、第三引数に処理対象の文字列を指定する。
    #文字列の両端（先頭、末尾）の指定した文字を削除するにはstrip()を使う。
    return re.sub(r'\s+', ' ', s).strip()

ebook_list = []

url = 'https://gihyo.jp/dp/genre/%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3'

sleep(3)

r = requests.get(url, timeout=3)

soup = BeautifulSoup(r.content, 'lxml')
page_urls = soup.select('#listBook > li > a')

for page_url in page_urls:
    page_url = 'https://gihyo.jp' + page_url.get('href')

    sleep(3)
        
    page_r = requests.get(page_url, timeout=3)
    page_soup = BeautifulSoup(page_r.content, 'lxml')

    title = page_soup.select_one('#title h1').text
    price_tag = page_soup.select_one('#productPrice > dt > span.buy').text
    price = price_tag.split('円')[0]+'円'
    contents =[normalize_spaces(h3.text) for h3 in page_soup.select('#content > h3')]

    print(url, title, price, contents)

    ebook_list.append({
    'url': url,
    'title': title,
    'price': price,
    'content': contents
    })
    print(ebook_list[-1])

df = pd.DataFrame(ebook_list)
df.to_csv('ebook_list.csv', index=None, encoding='utf-8-sig')