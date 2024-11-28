from pyautogui import *

f = open('ログ.txt', 'a', encoding='utf-8')

while True:
    n_point = input('座標名：')
    if n_point == 'END':
        break
    point = position()
    f.write(f'{n_point}:\t\t{point}\n')

f.close()