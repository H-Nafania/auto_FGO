from pyautogui import locateAllOnScreen

def tp(name: str):
    path = '.\\temp'
    return f'{path}\\{name}.png'

def accurate(png_name):
    png_name = tp(png_name)
    best_confidence = 0.0
    step = 0.1  # 大きなステップで開始
    min_confidence = 0.6  # 最小のconfidence値を設定
    max_confidence = 0.99  # 最大のconfidence値を設定

    
    while step >= 0.01:  # ステップが0.01以上の間繰り返す
        i = max_confidence
        while i >= min_confidence:
            try:
                matches = list(locateAllOnScreen(png_name, confidence=i))
            except Exception as e:
                matches = False
                print(f'エラーが発生しました: {e}')
            if matches and len(matches) > 3:
                best_confidence = i
                min_confidence = i  # 新しい最小値を設定
                break
            i -= step

        step /= 10  # ステップを細かくする


    print(f'最良の信頼度: {best_confidence}')

accurate('attack_back')