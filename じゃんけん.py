import random

d = {0: 'グー', 1: 'チョキ', 2: 'パー'}
options = tuple(d.keys())

win = 0
count = 0

print('*'*10 + f'\n選択肢：{d}\n' + '*'*10)

for _ in range(0, 3):
  computer_hand = random.choice(options)
  my_hand = 99
  while my_hand not in options:
    my_hand = input('自分が出す手を入力してください(整数 : 0, 1, 2) >')
    try:
      my_hand = int(my_hand)
    except:
      print('整数の0, 1, 2を入力してください')
  count += 1

  print(f'コンピューターが出した手：{d[computer_hand]}')
  print(f'自分が出した手：{d[my_hand]}')

  is_win = False
  if computer_hand == my_hand:
    is_win = 'あいこ'
  else:
    if computer_hand == 0 and my_hand == 2:
      is_win = True
    elif computer_hand == 1 and my_hand == 0:
      is_win = True
    elif computer_hand == 2 and my_hand ==1:
      is_win = True
  if isinstance(is_win, bool):
    is_win = '勝ち' if is_win else '負け'

  print(f'結果：{is_win}')
  if is_win == '勝ち':
    win += 1

print('*'*10 + f'\n勝った回数は{win}回です\n' + '*'*10)