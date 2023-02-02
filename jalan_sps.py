from time import sleep

import requests
from bs4 import BeautifulSoup
import pandas as pd

hotel_list = []

# year = input('チェックインする年を入力してください：')
month = input('チェックインする月を入力してください：')
day = input('チェックインする日を入力してください：')
stay_count = input('泊数を入力してください：')
room_count = input('室数を入力してください：')
adult_num = input('人数を入力してください：')

base_url = 'https://www.jalan.net/040000/LRG_040200/SML_040202/?screenId=UWW1402&distCd=01&listId=0&activeSort=0&mvTabFlg=1&stayYear=2023&stayMonth=' + month + '&stayDay=' + day + '&stayCount=' + stay_count + '&roomCount=' + room_count +'&adultNum=' + adult_num +'&yadHb=1&roomCrack=200000&kenCd=040000&lrgCd=040200&smlCd=040202&vosFlg=6&idx={}'

sleep(3)

r = requests.get(base_url, timeout=7.5)
if r.status_code >= 400:
    print(F'{base_url}は無効です')

soup = BeautifulSoup(r.content, 'lxml')

number = soup.select_one('td.jlnpc-planListCnt-header > span.s16_F60b').text
max_page_index = int(number) // 30 + 1
# print(max_page_index)

for i in range(max_page_index):
    url = base_url.format(30*i)

    sleep(3)

    page_r = requests.get(url, timeout=7.5)
    if page_r.status_code >= 400:
        print(F'{url}は無効です')
        continue

    page_soup = BeautifulSoup(page_r.content, 'lxml')

    #最安料金と1人あたりの料金
    table_soup = page_soup.select('div.p-yadoCassette__body.p-searchResultItem__body')
    for table in table_soup:
        hotel = table.select_one('a > div > div > div.p-searchResultItem__summaryInner > div.p-searchResultItem__summaryLeft > h2').text
        room_price = table.select_one('a > div > div > div.p-searchResultItem__summaryInner > div.p-searchResultItem__summaryRight > dl > dd > span.p-searchResultItem__lowestPriceValue').text
        per_price = table.select_one('a > div > div > div.p-searchResultItem__summaryInner > div.p-searchResultItem__summaryRight > dl > dd > span.p-searchResultItem__lowestUnitPrice').text
        page_urls = table.select('a.jlnpc-yadoCassette__link')
        # print(hotel,room_price,per_price,page_urls)
        
        # sleep(3)

        for i, page_url in enumerate(page_urls):
            page_url = 'https://www.jalan.net' + page_url.get('href')

            sleep(3)

            hotel_page_r = requests.get(page_url, timeout=7.5)
            if hotel_page_r.status_code >= 400:
                print(F'{page_url}は無効です')
                continue
        
            #ホテル名
            hotel_page_soup = BeautifulSoup(hotel_page_r.content, 'lxml')
            # hotel_name = hotel_page_soup.select_one('#pankuzu > h1').text

            #住所
            address_tags = hotel_page_soup.select_one('#jlnpc-main-contets-area > div.shisetsu-accesspartking_body_wrap > table tr:nth-child(1) > td').text
            if address_tags == None:
                continue

            else: 
            # address = address_tags.text
                address = address_tags.replace('大きな地図をみる', '')
                address = address.strip()
        
            #駐車場
            parking_tags = hotel_page_soup.select_one('#jlnpc-main-contets-area > div.shisetsu-accesspartking_body_wrap > table tr:nth-child(3) > td').text  
            if parking_tags == None:
                continue

            else:
                parking = parking_tags.replace('\n','')
                parking = parking.strip()

            #タイプ別の室数
            room_tag = hotel_page_soup.select_one('.shisetsu-roomsetsubi_body')
            tags = room_tag.text

            if '総部屋数' not in tags:
                single = room_tag.select_one('tr:nth-child(2) > td > div > table tr:nth-child(2) > td:first-child').text
                double = room_tag.select_one('tr:nth-child(2) > td > div > table tr:nth-child(2) > td:nth-child(2)').text
                twin = room_tag.select_one('tr:nth-child(2) > td > div > table tr:nth-child(2) > td:nth-child(3)').text
                sweet = room_tag.select_one('tr:nth-child(2) > td > div > table tr:nth-child(2) > td:last-child').text
                total = None

            elif 'シングル' not in tags:
                single = None
                double = None
                twin = None
                sweet = None
                total = room_tag.select_one('tr:nth-child(1) > td > div > table tr:nth-child(2) > td:nth-child(5)').text
                total = total.strip()

            else:
                single = room_tag.select_one('tr:nth-child(3) > td > div > table tr:nth-child(2) > td:first-child').text
                double = room_tag.select_one('tr:nth-child(3) > td > div > table tr:nth-child(2) > td:nth-child(2)').text
                twin = room_tag.select_one('tr:nth-child(3) > td > div > table tr:nth-child(2) > td:nth-child(3)').text
                sweet = room_tag.select_one('tr:nth-child(3) > td > div > table tr:nth-child(2) > td:last-child').text
                total = room_tag.select_one('tr:nth-child(1) > td > div > table tr:nth-child(2) > td:nth-child(5)').text
                total = total.strip()

            # sleep(3)

            hotel_list.append({
                'ホテル名': hotel,
                '詳細ページ': page_url,
                '住所': address,
                'シングル': single,
                'ダブル': double,
                'ツイン': twin,
                'スイート': sweet,
                '総部屋数': total,
                '室料': room_price,
                '1人あたり': per_price,
                '駐車場': parking
            })
            print(hotel_list[-1])

#スプレッドシート出力
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# データフレームをGoogleスプレッドシートに書き出す
from gspread_dataframe import set_with_dataframe

#認証
SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'virtual-firefly-363001-cb50276b19b7.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
gs = gspread.authorize(credentials)
SPREADSHEET_KEY = '18eKi7qv6vwsT_E2OQbSrIJdn_qyISrJyAlNOiu1QctA'

#書込
df = pd.DataFrame(hotel_list)
workbook = gs.open_by_key(SPREADSHEET_KEY)
set_with_dataframe(workbook.worksheet("シート1"), df, include_index=False)