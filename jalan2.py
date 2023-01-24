from time import sleep

import requests
from bs4 import BeautifulSoup
import pandas as pd

max_page_index = 2
price_list =  []
hotel_list = []

base_url = 'https://www.jalan.net/040000/LRG_040200/SML_040202/?screenId=UWW1402&distCd=01&listId=0&activeSort=0&mvTabFlg=1&stayYear=2023&stayMonth=6&stayDay=23&stayCount=2&roomCount=1&adultNum=2&yadHb=1&roomCrack=200000&kenCd=040000&lrgCd=040200&smlCd=040202&vosFlg=6&idx={}'

for i in range(max_page_index):
    url = base_url.format(30*i)

    sleep(3)

    r = requests.get(url, timeout=7.5)
    if r.status_code >= 400:
        print(F'{url}は無効です')
        continue

    soup = BeautifulSoup(r.content, 'lxml')

    #最安料金と1人あたりの料金
    table_soup = soup.select('div.p-yadoCassette__body.p-searchResultItem__body')
    for table in table_soup:
        hotel = table.select_one('div.p-yadoCassette__body.p-searchResultItem__body > a > div > div > div.p-searchResultItem__summaryInner > div.p-searchResultItem__summaryLeft > h2').text
        room_prices = table.select_one('div.p-yadoCassette__body.p-searchResultItem__body > a > div > div > div.p-searchResultItem__summaryInner > div.p-searchResultItem__summaryRight > dl > dd > span.p-searchResultItem__lowestPriceValue').text
        per_prices = table.select_one('div.p-yadoCassette__body.p-searchResultItem__body > a > div > div > div.p-searchResultItem__summaryInner > div.p-searchResultItem__summaryRight > dl > dd > span.p-searchResultItem__lowestUnitPrice').text
        page_urls = table.select('div.p-yadoCassette__body.p-searchResultItem__body > a.jlnpc-yadoCassette__link')
        sleep(3)

        price_list.append({
            'ホテル名' :hotel,
            '室料' : room_prices,
            '1人あたり' : per_prices
        })
        # print(price_list[-1])

        for i, page_url in enumerate(page_urls):
            page_url = 'https://www.jalan.net' + page_url.get('href')

            sleep(3)

            page_r = requests.get(page_url, timeout=7.5)
            if page_r.status_code >= 400:
                print(F'{page_url}は無効です')
                continue
        
            #ホテル名
            page_soup = BeautifulSoup(page_r.content, 'lxml')
            hotel_name = page_soup.select_one('#pankuzu > h1').text
        
            #タイプ別の室数
            room_tags = page_soup.select_one('.shisetsu-roomsetsubi_body')
            tags = room_tags.text

            if '総部屋数' not in tags:
                single = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(2) > td > div > table tr:nth-child(2) > td:first-child').text
                double = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(2) > td > div > table tr:nth-child(2) > td:nth-child(2)').text
                twin = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(2) > td > div > table tr:nth-child(2) > td:nth-child(3)').text
                sweet = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(2) > td > div > table tr:nth-child(2) > td:last-child').text
                total = None

            elif 'シングル' not in tags:
                single = None
                double = None
                twin = None
                sweet = None
                total = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(1) > td > div > table tr:nth-child(2) > td:nth-child(5)').text
                total = total.strip()

            else:
                single = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(3) > td > div > table tr:nth-child(2) > td:first-child').text
                double = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(3) > td > div > table tr:nth-child(2) > td:nth-child(2)').text
                twin = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(3) > td > div > table tr:nth-child(2) > td:nth-child(3)').text
                sweet = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(3) > td > div > table tr:nth-child(2) > td:last-child').text
                total = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(1) > td > div > table tr:nth-child(2) > td:nth-child(5)').text
                total = total.strip()

            sleep(3)

            for item in price_list:
                if item['ホテル名'] == hotel_name:
                    r_price = item['室料']
                    p_price = item['1人あたり']

            hotel_list.append({
                'ホテル名': hotel_name,
                'シングル': single,
                'ダブル': double,
                'ツイン': twin,
                'スイート': sweet,
                '総部屋数': total,
                '室料': r_price,
                '1人あたり': p_price
            })
            print(hotel_list[-1])

#csv出力
df = pd.DataFrame(hotel_list)
df.to_csv('list.csv', index=False, encoding='utf-8-sig')