import tkinter
from tkinter import RIGHT, END, DISABLED
from tkinter.constants import NORMAL
from decimal import Decimal
from tkmacosx import Button

#ウインドウの作成
root = tkinter.Tk()
root.title('電卓')
root.iconbitmap('calculator.ico')
root.geometry('540x395')
root.resizable(0, 0)

#関数の定義
def clear_number():
    screen.delete(0, END)
    #.の入力ロックを解除
    unlock_button()

def negate():
    calculated_number = -1 * float(screen.get())
    # 結果を表示するため現在のスクリーンに表示されている数字を削除
    screen.delete(0, END)
    screen.insert(0, calculated_number)

def percentage():
    calculated_number = 0.01 * float(screen.get())
    # 結果を表示するため現在のスクリーンに表示されている数字を削除
    screen.delete(0, END)
    screen.insert(0, calculated_number)

def add_element(number):
    screen.insert(END, number)

    # .が挿入された場合それ以降点を挿入できなくする
    if '.' in screen.get():
        decimal_button.config(state=DISABLED)
    
#入力ロック解除
def unlock_button():
    add_button.config(state=NORMAL)
    substract_button.config(state=NORMAL)
    multiply_button.config(state=NORMAL)
    divide_button.config(state=NORMAL)

    decimal_button.config(state=NORMAL)

#割り算や掛け算などの演算子ボタンが押された時の処理
def operate(operator):
    #グローバル変数宣言
    global operation, first_number
    #演算の種類と入力された数字の保持
    operation = operator
    first_number = screen.get()

    #最初の数字を削除
    screen.delete(0, END)

    # =またはclearが押されるまで演算ボタンを押せなくする処理
    add_button.config(state=DISABLED)
    substract_button.config(state=DISABLED)
    multiply_button.config(state=DISABLED)
    divide_button.config(state=DISABLED)
    # 演算子が押された時は.のロックを解除
    decimal_button.config(state=NORMAL)

def calculate():
    #演算の実行
    if operation == 'add':
        calculated_number = Decimal(first_number) + Decimal(screen.get())
    elif operation == 'substract':
        calculated_number = Decimal(first_number) - Decimal(screen.get())
    elif operation == 'multiply':
        calculated_number = Decimal(first_number) * Decimal(screen.get())
    elif operation == 'divide':
        #分母に0が来ているかどうかの判定
        if screen.get() == '0':
            calculated_number = 'ERROR'
        else:
            calculated_number = Decimal(first_number) / Decimal(screen.get())

    #計算結果を表示するために現在スクリーンに表示されている数字を削除
    screen.delete(0, END)
    screen.insert(0, calculated_number)

    #ボタンのロック解除
    unlock_button()
    

#色とフォントの設定
screen_font = ('Segoe UI', 30, 'bold')
button_font = ('Segoe UI', 20, 'bold')
light_orange = '#FFEFD5'
light_gray = '#DCDCDC'
orange = '#ffa500'
black = '#000000'
white = '#FFFFFF'

#フレームの作成
screen_frame = tkinter.LabelFrame(root)
button_frame = tkinter.LabelFrame(root)
screen_frame.pack(padx=2, pady=(5, 0))
button_frame.pack(padx=2)
# button_frame.pack(fill='both', expand=True, padx=2, pady=5)

#エントリーの作成
screen = tkinter.Entry(screen_frame, width=40, font=screen_font, bg=light_orange, justify=RIGHT, borderwidth=5) #justifyは文字の右寄せに使う。要ライブラリのインポート
screen.pack()

#ボタンの作成
clear_button = Button(button_frame, text='C', font=button_font, bg=light_gray, command=clear_number)
negate_button = Button(button_frame, text='+/-', font=button_font, bg=light_gray, command=negate)
percentage_button = Button(button_frame, text='%', font=button_font, bg=light_gray, command=percentage)
divide_button = Button(button_frame, text='÷', font=button_font, bg=orange, fg=black, command=lambda: operate('divide'))
seven_button = Button(button_frame, text='7', font=button_font, bg=black, fg=white, command=lambda: add_element(7))
eight_button = Button(button_frame, text='8', font=button_font, bg=black, fg=white, command=lambda: add_element(8))
nine_button = Button(button_frame, text='9', font=button_font, bg=black, fg=white, command=lambda: add_element(9))
multiply_button = Button(button_frame, text='×', font=button_font, bg=orange, fg=black, command=lambda: operate('multiply'))
four_button = Button(button_frame, text='4', font=button_font, bg=black, fg=white, command=lambda: add_element(4))
five_button = Button(button_frame, text='5', font=button_font, bg=black, fg=white, command=lambda: add_element(5))
six_button = Button(button_frame, text='6', font=button_font, bg=black, fg=white, command=lambda: add_element(6))
substract_button = Button(button_frame, text='-', font=button_font, bg=orange, fg=black, command=lambda: operate('substract'))
one_button = Button(button_frame, text='1', font=button_font, bg=black, fg=white, command=lambda: add_element(1))
two_button = Button(button_frame, text='2', font=button_font, bg=black, fg=white, command=lambda: add_element(2))
three_button = Button(button_frame, text='3', font=button_font, bg=black, fg=white, command=lambda: add_element(3))
add_button = Button(button_frame, text='+', font=button_font, bg=orange, fg=black, command=lambda: operate('add'))
zero_button = Button(button_frame, text='0', font=button_font, bg=black, fg=white, command=lambda: add_element(0))
decimal_button = Button(button_frame, text='.', font=button_font, bg=black, fg=white, command=lambda: add_element('.'))
equal_button = Button(button_frame, text='=', font=button_font, bg=orange, fg=black, command=calculate)

#1行目の配置
clear_button.grid(row=0, column=0, sticky='WE', pady=1, ipady=15)
negate_button.grid(row=0, column=1, sticky='WE', pady=1, ipady=15)
percentage_button.grid(row=0, column=2, sticky='WE', pady=1, ipady=15)
divide_button.grid(row=0, column=3, sticky='WE', pady=1, ipady=15)

#2行目の配置(ボタンの引き伸ばしをipadxで)
seven_button.grid(row=1, column=0, sticky='WE', ipadx=3, pady=1, ipady=15)
eight_button.grid(row=1, column=1, sticky='WE', ipadx=3, pady=1, ipady=15)
nine_button.grid(row=1, column=2, sticky='WE', ipadx=3, pady=1, ipady=15)
multiply_button.grid(row=1, column=3, sticky='WE', ipadx=3, pady=1, ipady=15)

#3行目の配置
four_button.grid(row=2, column=0, sticky='WE', pady=1, ipady=15)
five_button.grid(row=2, column=1, sticky='WE', pady=1, ipady=15)
six_button.grid(row=2, column=2, sticky='WE', pady=1, ipady=15)
substract_button.grid(row=2, column=3, sticky='WE', pady=1, ipady=15)

#4行目の配置
one_button.grid(row=3, column=0, sticky='WE', pady=1, ipady=15)
two_button.grid(row=3, column=1, sticky='WE', pady=1, ipady=15)
three_button.grid(row=3, column=2, sticky='WE', pady=1, ipady=15)
add_button.grid(row=3, column=3, sticky='WE', pady=1, ipady=15)

#5行目の配置（ゼロボタンの引き伸ばしをcolumnspanで）
zero_button.grid(row=4, column=0, sticky='WE', columnspan=2, pady=1, ipady=15)
decimal_button.grid(row=4, column=2, sticky='WE', pady=1, ipady=15)
equal_button.grid(row=4, column=3, sticky='WE', pady=1, ipady=15)

#ウインドウのループ処理
root.mainloop()