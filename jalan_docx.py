import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pandas as pd

# wordファイルを新規作成
doc = docx.Document()

#ファイルの取得
df = pd.read_csv('list.csv')  

for i, r in df.iterrows():
    # print(r['ホテル名'], r['詳細ページ'])
    if i == '':
        break

    doc.add_paragraph('ホテル名：'+ r['ホテル名'])
    doc.add_paragraph('詳細ページ：'+ r['詳細ページ'])
    doc.add_paragraph('住所：'+ r['住所'])
    doc.add_paragraph('シングル：'+ str(r['シングル']))
    doc.add_paragraph('ダブル：'+ str(r['ダブル']))
    doc.add_paragraph('ツイン：'+ str(r['ツイン']))
    doc.add_paragraph('スイート：'+ str(r['スイート']))
    doc.add_paragraph('総部屋数：'+ str(r['総部屋数']))
    doc.add_paragraph('室料：'+ str(r['室料']))
    doc.add_paragraph('1人あたり：'+ str(r['1人あたり']))
    doc.add_paragraph('駐車場：'+ r['駐車場'])

    # 改ページ
    doc.add_page_break()

# すべての行をセンタリング
for p in doc.paragraphs:
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
# ファイルを保存
doc.save('hotel_list.docx')