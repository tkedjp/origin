from time import sleep

import requests
from bs4 import BeautifulSoup

url = 'https://qiita.com/advent-calendar/2016/crawler'

r = requests.get(url, timeout=3)
r.raise_for_status()

soup = BeautifulSoup(r.content, 'lxml')

page_tags = soup.select('div.adventCalendarItem_calendarContent')

for page_tag in page_tags:
    url_tags = page_tag.select('div.adventCalendarItem_commentWrapper > .adventCalendarItem_entry > a')
    author_tags = page_tag.select('a.adventCalendarItem_author')

    for author_tag in author_tags:
        author = author_tag.text

        for url_tag in url_tags:
            page_url = url_tag.get('href')
            page_title = page_tag.text
            print(author, page_url, page_title)