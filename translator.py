import tkinter
from tkinter import ttk
from googletrans import Translator
from tkmacosx import Button
from tkinter import filedialog

#翻訳用のインスタンス
translator = Translator()

#ウインドウの作成
root = tkinter.Tk()
root.title('翻訳アプリ')
root.iconbitmap('translator.ico')
root.geometry('590x480')
root.resizable(0, 0)

# 色&フォントの設定
normal_font = ('Arial', 10)
bold_font = ('Arial', 10, 'bold')
bg_color = '#87CEFA'
button_color = '#4682B4'
root.config(bg=bg_color)

#関数の定義
def convert():
    languages = {
        '日本語': 'ja',
        '英語': 'en',
        '中国語': 'zh-ch',
        'フランス語': 'fr',
        'ドイツ語': 'de',
        'ヒンディー語': 'hi'
    }

    #翻訳したい文章の取得(end-1cとは終了地点のこと)
    before_text = input_box.get('1.0', 'end-1c')
    before_language = input_pulldown.get()
    after_language = output_pulldown.get()
    # print(before_text)
    # print(before_language)
    # print(after_language)

    after_text = translator.translate(before_text, src=languages[before_language], dest=languages[after_language])
    output_box.insert('1.0', after_text.text)

def save():
    file_name = filedialog.asksaveasfilename(title='名前をつけて保存', filetypes=[('Text', '.txt'), ('PNG', '.png')], initialdir='./', defaultextension='.txt')
    with open(file_name, 'w') as f:
        f.write(output_box.get('1.0', 'end-1c'))


#プルダウンの作成
language_list = ['日本語', '英語', '中国語', 'フランス語', 'ドイツ語', 'ヒンディー語']

input_pulldown = ttk.Combobox(root, value=language_list, font=normal_font, justify='center')
output_pulldown = ttk.Combobox(root, value=language_list, font=normal_font, justify='center')
to_label = tkinter.Label(root, text='to', font=normal_font, bg=bg_color)
input_pulldown.grid(row=0, column=0, padx=10)
to_label.grid(row=0, column=1, padx=10)
output_pulldown.grid(row=0, column=2, padx=10)

input_pulldown.set('日本語')
output_pulldown.set('英語')

# 入力&出力欄の作成
input_box = tkinter.Text(root, font=normal_font, width=40, height=20, borderwidth=3)
output_box = tkinter.Text(root, font=normal_font, width=40, height=20, borderwidth=3)
equal_sign = tkinter.Label(root, text='=', font=normal_font, bg=bg_color)

input_box.grid(row=1, column=0, padx=10, pady=10)
equal_sign.grid(row=1, column=1)
output_box.grid(row=1, column=2, padx=10, pady=10)

#表示したい文字の設定。第1引数で行と列を指定し，第2引数で文字を指定。
input_box.insert('1.0', '翻訳したい文章を入力\n')

#ボタンの作成
convert_button = Button(root, text='翻訳', font=bold_font, bg=button_color, fg='white', command=convert)
save_button = Button(root, text='保存', font=bold_font, bg=button_color, fg='white', command=save)
convert_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, ipadx=50)
save_button.grid(row=3, column=0, columnspan=3, padx=10, pady=(0, 10), ipadx=50)

#ウインドウのループ処理
root.mainloop()