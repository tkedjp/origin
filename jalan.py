from time import sleep

import requests
from bs4 import BeautifulSoup
import pandas as pd

max_page_index = 2
hotel_list = []

base_url = 'https://www.jalan.net/040000/LRG_040200/SML_040202/?screenId=UWW1402&distCd=01&listId=0&activeSort=0&mvTabFlg=1&stayYear=2023&stayMonth=6&stayDay=23&stayCount=2&roomCount=1&adultNum=2&yadHb=1&roomCrack=200000&kenCd=040000&lrgCd=040200&smlCd=040202&vosFlg=6&idx={}'

for i in range(max_page_index):
    # print('hotel_list:', len(hotel_list))
    url = base_url.format(30*i)

    sleep(3)

    r = requests.get(url, timeout=7.5)
    if r.status_code >= 400:
        print(F'{url}は無効です')
        continue

    soup = BeautifulSoup(r.content, 'lxml')
    page_urls = soup.select('.jlnpc-yadoCassette__link')
    # print(page_urls)

    for i, page_url in enumerate(page_urls):
        page_url = 'https://www.jalan.net' + page_url.get('href')

        sleep(3)

        page_r = requests.get(page_url, timeout=7.5)
        if page_r.status_code >= 400:
            print(F'{page_url}は無効です')
            continue

        page_soup = BeautifulSoup(page_r.content, 'lxml')
        hotel_name = page_soup.select_one('#pankuzu > h1').text
        
        room_tags = page_soup.select_one('.shisetsu-roomsetsubi_body')

        if '総部屋数' not in room_tags:
            single = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(2) > td > div > table tr:nth-child(2) > td:first-child')
            double = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(2) > td > div > table tr:nth-child(2) > td:nth-child(2)')
            twin = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(2) > td > div > table tr:nth-child(2) > td:nth-child(3)')
            sweet = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(2) > td > div > table tr:nth-child(2) > td:last-child')
 
            sleep(3)

        elif 'シングル' not in room_tags:
            single = None
            double = None
            twin = None
            sweet = None

            sleep(3)

        else:
            single = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(3) > td > div > table tr:nth-child(2) > td:first-child')
            double = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(3) > td > div > table tr:nth-child(2) > td:nth-child(2)')
            twin = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(3) > td > div > table tr:nth-child(2) > td:nth-child(3)')
            sweet = room_tags.select_one('.shisetsu-roomsetsubi_body > tr:nth-child(3) > td > div > table tr:nth-child(2) > td:last-child')
            
            sleep(3)
        
        print(hotel_name,single,double,twin,sweet)