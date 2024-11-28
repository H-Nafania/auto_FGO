import os
from time import *
from pyautogui import *
import datetime
import random

"""
def tp(name: str):
    path = '.\\temp'
    return f'{path}\\{name}.png'
"""


def tp(name: str):
    path = '.\\temp'
    return f'{path}\\{name}.png'


region_icon = locateOnScreen(tp('defult'), confidence=0.9)
global px, py, region
px = region_icon[0]
py = region_icon[1]
region = (px, py, 1820, 850)


def until_click_X(png_path: str, multi_click=1, rta=True, max_attempts=5, confidence=0.9, region=region):
    """
    指定された画像が見つかるまで繰り返し検索し、見つかったらクリックする関数。
    :param png_path: クリック対象の画像パス
    :param multi_click: 一度に行うクリックの数
    :param rta: 画像が見つからなくなるまで繰り返すかどうか
    :param max_attempts: 最大試行回数
    :param confidence: 画像検出の信頼度
    :param region: 検索する画面領域
    :return: クリック成功の有無
    """
    png_path = tp(png_path)
    for attempt in range(max_attempts):
        try:
            point = locateCenterOnScreen(
                png_path, confidence=confidence, region=region)
            if point:
                _click_point(point, multi_click)
                if not rta:
                    return True
                if _is_image_absent(png_path, confidence, region):
                    return True
            else:
                print(f'残り試行回数：{max_attempts - attempt}')
                sleep(0.5)
        except ImageNotFoundException:
            print(f'残り試行回数：{max_attempts - attempt}')
            sleep(0.5)

    print(f'{png_path}未発見')
    return False


def _click_point(point, times=1):
    """ 指定された位置を指定された回数クリックするヘルパー関数 """
    for t in range(times):
        click(point)
        sleep(0.5)
        print(f'クリック：{t + 1}')


def _is_image_absent(png_path, confidence, region=region):
    """ 画像が画面上に存在しないかを確認するヘルパー関数 """
    try:
        return locateCenterOnScreen(png_path, confidence=confidence, region=region) is None
    except ImageNotFoundException:
        return True


def until_check_png(png: str, try_time=1000, confidence=0.9, clickmid=False, region=region, waiting_time=0.2):
    t = 0
    png_path = tp(png)  # tp 関数の定義が不明ですが、おそらく画像のパスを取得する関数と仮定します
    while t < try_time:
        try:
            if locateOnScreen(png_path, confidence=confidence, region=region):
                return True
        except ImageNotFoundException:
            pass
        print(f'{png}\tmiss:{t}')
        if clickmid is not False:
            # px, py が未定義ですが、これらはおそらくスクリプトのどこかで定義されていると仮定します
            click(px+972, py+298) if type(clickmid) == bool else click(clickmid)
        sleep(waiting_time)
        t += 1

    return False


def un_check_png(png: str, try_time=1000, confidence=0.9, clickmid=False, region=region, waiting_time=0.2):
    png_path = tp(png)
    i = 1
    while i < try_time:
        try:
            if locateOnScreen(png_path, confidence=confidence, region=region):
                pass
        except ImageNotFoundException:
            print(f'{png} seccess')
            return True
        print(f'{png}\tnot dispear:{i}')
        if clickmid is not False:
            click(px+972, py+298) if type(clickmid) == bool else click(clickmid)
        sleep(waiting_time)
        i += 1


def unique_locations(images, tolerance=50):

    images = [i for i in images]

    if not images:
        return []

    # Sort locations by their coordinates for easier comparison
    images = sorted(images, key=lambda x: (x.left, x.top))

    unique = [images[0]]

    for current in images[1:]:
        last = unique[-1]

        # Calculate the distance between current and last location
        distance = ((current.left - last.left)**2 +
                    (current.top - last.top)**2)**0.5

        if distance > tolerance:
            unique.append(current)

    return unique


class Samsara:
    def __init__(self):
        self.atk = (px + 1561, py + 723)
        self.SKILL_COORDS = {
            "servant1": {"skill1": (px + 140, py + 666), "skill2": (px + 245, py + 666), "skill3": (px + 350, py + 666)},
            "servant2": {"skill1": (px + 500, py + 666), "skill2": (px + 605, py + 666), "skill3": (px + 710, py + 666)},
            "servant3": {"skill1": (px + 860, py + 666), "skill2": (px + 965, py + 666), "skill3": (px + 1070, py + 666)}
        }
        self.NOBLE_PHANTASM_COORDS = {
            "NP1": (px + 655, py + 250),
            "NP2": (px + 915, py + 250),
            "NP3": (px + 1175, py + 250)
        }
        self.SKILL_DIRECTIVE_COORDS = {
            "to_servant1": (px + 565, py + 490),
            "to_servant2": (px + 915, py + 490),
            "to_servant3": (px + 1265, py + 490)
        }
        self.MASTER_SKILL_COORDS = {
            "master": (px + 1652, py + 390),
            "master1": (px + 1325, py + 390),
            "master2": (px + 1432, py + 390),
            "master3": (px + 1512, py + 390)
        }
        self.ORDER_CHANGE = {
            "oc1": (px + 340, py + 430),
            "oc2": (px + 566, py + 430),
            "oc3": (px + 792, py + 430),
            "oc4": (px + 1018, py + 430),
            "oc5": (px + 1244, py + 430),
            "oc6": (px + 1470, py + 430)
        }
        self.CARD_NORMAL = {
            "card1": (px + 333, py + 580),
            "card2": (px + 624, py + 580),
            "card3": (px + 915, py + 580),
            "card4": (px + 1206, py + 580),
            "card5": (px + 1497, py + 580)
        }

    def skill(self, servant_number, skill_number, directive=0):

        until_check_png('attack')

        coords = self.SKILL_COORDS[f"servant{
            servant_number}"][f"skill{skill_number}"]
        if directive != 0:
            until_check_png('batsu', clickmid=coords)
            coords_d = self.SKILL_DIRECTIVE_COORDS[f"to_servant{directive}"]
            un_check_png('batsu', clickmid=coords_d)
            sleep(0.3)
            until_check_png('attack', clickmid=True)

        elif directive == 0:
            until_check_png("master_skill")
            un_check_png('master_skill', clickmid=coords, confidence=0.8)
            until_check_png('master_skill', clickmid=True)
        else:
            raise ValueError(f"Unknown directive: {directive}")

    def skill_kkr(self, servant_number, skill_number, directive=0):

        until_check_png('attack')

        coords = self.SKILL_COORDS[f"servant{
            servant_number}"][f"skill{skill_number}"]
        if directive != 0:
            until_check_png('batsu', clickmid=coords)
            until_click_X('no_star')
            coords_d = self.SKILL_DIRECTIVE_COORDS[f"to_servant{directive}"]
            un_check_png("batsu", clickmid=coords_d)
            sleep(0.3)
            until_check_png('attack', clickmid=True)

        elif directive == 0:
            until_check_png('batsu', clickmid=coords)
            until_click_X('10_star', multi_click=2)
        else:
            raise ValueError(f"Unknown directive: {directive}")

    def skill_ex(self, servant_number, skill_number, np_type="person"):  # np_typeは「person」または「army」

        until_check_png('attack')

        anti_png = 'anti_army' if np_type == 'army' else 'anti_person'
        coords = self.SKILL_COORDS[f"servant{
            servant_number}"][f"skill{skill_number}"]
        until_check_png('batsu', clickmid=coords)
        until_click_X(anti_png, multi_click=2)
        sleep(0.3)
        until_check_png('master_skill', clickmid=True)

    def master_skill(self, skill_number, directive=0):

        until_check_png('master_skill')
        sleep(0.5)
        click(self.MASTER_SKILL_COORDS["master"])
        sleep(0.5)

        coords = self.MASTER_SKILL_COORDS[f"master{skill_number}"]
        if directive == 0:
            un_check_png("master_skill", clickmid=coords, confidence=0.8)
            until_check_png("attack", clickmid=True)

        elif type(directive) == list:
            until_check_png('batsu', clickmid=coords)
            sleep(0.3)
            for coords_oc in directive:
                click(self.ORDER_CHANGE[f"oc{coords_oc}"])
            until_click_X('change', multi_click=2)
            until_check_png("attack", clickmid=True)

        elif type(directive) == int:
            until_check_png('batsu', clickmid=coords)
            coord_t = self.SKILL_DIRECTIVE_COORDS[f"to_servant{directive}"]
            un_check_png('batsu', clickmid=coord_t)
            until_check_png("master_skill", clickmid=True)

        else:
            raise ValueError(f"Unknown directive: {directive}")

    def np_attack(self, np_number, ciel=False, order=1):
        until_check_png('attack')
        until_check_png('attack_back', clickmid=self.atk, confidence=0.75)
        if type(np_number) != list:
            np_number = [np_number]
        for np in np_number:
            click(self.NOBLE_PHANTASM_COORDS[f"NP{np}"])
            sleep(0.1)

        for cards_number in random.sample([1, 2, 3, 4, 5], 3 - len(np_number)):
            click(self.CARD_NORMAL[f"card{cards_number}"])
            sleep(0.1)

        sleep(8)


class Loop_type(Samsara):
    def __init__(self):
        super().__init__()

    def template(self):
        until_check_png("master_skill")
        until_check_png('attack')
        sleep(1)

        # 1
        print("turn1 skill")

        # self.skill(servant_number=1, skill_number=1, directive=0)
        # self.skill(servant_number=1, skill_number=2, directive=0)
        # self.skill(servant_number=1, skill_number=3, directive=1)

        # self.skill(servant_number=2, skill_number=1, directive=1)
        # self.skill(servant_number=2, skill_number=2, directive=0)
        # self.skill(servant_number=2, skill_number=3, directive=0)

        # self.skill(servant_number=3, skill_number=1, directive=1)
        # self.skill(servant_number=3, skill_number=2, directive=0)
        # self.skill(servant_number=3, skill_number=3, directive=0)

        # self.master_skill(skill_number=1, directive=1)

        print("turn1 attack")

        self.np_attack(np_number=1)

        # 2
        print("turn2 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        # self.skill(servant_number=1, skill_number=1, directive=0)
        # self.skill(servant_number=1, skill_number=2, directive=0)
        # self.skill(servant_number=1, skill_number=3, directive=1)

        # self.skill(servant_number=2, skill_number=1, directive=1)
        # self.skill(servant_number=2, skill_number=2, directive=0)
        # self.skill(servant_number=2, skill_number=3, directive=0)

        # self.skill(servant_number=3, skill_number=1, directive=1)
        # self.skill(servant_number=3, skill_number=2, directive=0)
        # self.skill(servant_number=3, skill_number=3, directive=0)

        # self.master_skill(skill_number=1, directive=1)

        print("turn2 attack")

        self.np_attack(np_number=1)

        # 3
        print("turn3 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        # self.skill(servant_number=1, skill_number=1, directive=0)
        # self.skill(servant_number=1, skill_number=2, directive=0)
        # self.skill(servant_number=1, skill_number=3, directive=1)

        # self.skill(servant_number=2, skill_number=1, directive=1)
        # self.skill(servant_number=2, skill_number=2, directive=0)
        # self.skill(servant_number=2, skill_number=3, directive=0)

        # self.skill(servant_number=3, skill_number=1, directive=1)
        # self.skill(servant_number=3, skill_number=2, directive=0)
        # self.skill(servant_number=3, skill_number=3, directive=0)

        # self.master_skill(skill_number=1, directive=1)

        print("turn3 attack")

        self.np_attack(np_number=1)

    def kkr_any(self):
        until_check_png("master_skill")
        until_check_png('attack')
        sleep(1)

        # 1
        print("turn1 skill")

        self.skill(servant_number=2, skill_number=2, directive=1)
        self.skill(servant_number=2, skill_number=3, directive=1)

        self.skill(servant_number=3, skill_number=2, directive=1)
        self.skill(servant_number=3, skill_number=3, directive=1)

        self.skill_kkr(servant_number=1, skill_number=1, directive=0)
        self.skill_kkr(servant_number=1, skill_number=2, directive=1)
        self.skill_kkr(servant_number=1, skill_number=3, directive=0)

        print("turn1 attack")

        self.np_attack(np_number=1)

        # 2
        print("turn2 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        self.skill(servant_number=2, skill_number=1, directive=1)
        self.skill(servant_number=3, skill_number=1, directive=1)

        self.master_skill(3, directive=[3, 4])

        self.skill(servant_number=3, skill_number=1, directive=0)
        self.skill_kkr(servant_number=1, skill_number=1, directive=0)

        print("turn2 attack")

        self.np_attack(np_number=1)

        # 3
        print("turn3 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        self.skill(servant_number=3, skill_number=2, directive=1)
        self.skill(servant_number=3, skill_number=3, directive=1)

        self.skill_kkr(servant_number=1, skill_number=2, directive=1)
        self.skill_kkr(servant_number=1, skill_number=3, directive=0)

        self.master_skill(skill_number=1)

        print("turn3 attack")

        self.np_attack(np_number=1)

    def fast(self):
        until_check_png("master_skill")
        until_check_png('attack')
        sleep(1)

        # 1
        print("turn1 skill")

        self.skill(servant_number=1, skill_number=3, directive=0)
        self.skill(servant_number=2, skill_number=1, directive=0)
        self.skill(servant_number=3, skill_number=1, directive=0)
        self.skill(servant_number=3, skill_number=3, directive=1)

        print("turn1 attack")

        self.np_attack(np_number=1)

        # 2
        print("turn2 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        print("turn2 attack")

        self.skill(servant_number=2, skill_number=3, directive=2)
        self.np_attack(np_number=2)

        # 3
        print("turn3 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        self.skill(servant_number=1, skill_number=1, directive=0)
        self.skill(servant_number=1, skill_number=2, directive=1)

        self.skill(servant_number=3, skill_number=2, directive=1)

        print("turn3 attack")

        self.np_attack(np_number=1)

    def santa(self):
        until_check_png("master_skill")
        until_check_png('attack')
        sleep(1)

        # 1
        print("turn1 skill")

        self.skill(servant_number=2, skill_number=1, directive=0)
        self.skill(servant_number=2, skill_number=2, directive=3)
        self.skill(servant_number=2, skill_number=3, directive=3)

        self.skill(servant_number=3, skill_number=3, directive=0)

        self.master_skill(skill_number=3, directive=[2, 5])

        self.skill(servant_number=2, skill_number=1, directive=0)

        print("turn1 attack")

        self.np_attack(np_number=1)

        # 2
        print("turn2 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        self.skill(servant_number=1, skill_number=3, directive=3)
        self.skill(servant_number=1, skill_number=1, directive=0)

        print("turn2 attack")

        self.np_attack(np_number=3)

        # 3
        print("turn3 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        self.skill(servant_number=3, skill_number=2, directive=0)
        self.skill(servant_number=3, skill_number=1, directive=0)

        self.skill(servant_number=2, skill_number=2, directive=3)
        self.skill(servant_number=2, skill_number=3, directive=3)

        self.master_skill(skill_number=1, directive=0)

        print("turn3 attack")

        self.np_attack(np_number=3)

    def odeko(self):
        until_check_png("master_skill")
        until_check_png('attack')
        sleep(1)

        # 1
        print("turn1 skill")

        self.skill(servant_number=1, skill_number=3, directive=0)

        self.skill(servant_number=2, skill_number=1, directive=0)
        self.skill(servant_number=2, skill_number=3, directive=0)

        self.skill(servant_number=3, skill_number=3, directive=0)

        print("turn1 attack")

        self.np_attack(np_number=1)

        # 2
        print("turn2 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        self.skill(servant_number=1, skill_number=1, directive=0)
        self.skill(servant_number=1, skill_number=2, directive=3)
        self.skill(servant_number=1, skill_number=3, directive=3)
        self.master_skill(skill_number=3, directive=[1, 5])
        self.skill(servant_number=1, skill_number=1, directive=0)
        self.skill(servant_number=1, skill_number=2, directive=3)
        self.skill(servant_number=1, skill_number=3, directive=3)

        self.skill(servant_number=2, skill_number=2, directive=3)

        print("turn2 attack")

        self.np_attack(np_number=[2, 3])

        # 3
        print("turn3 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        self.skill(servant_number=3, skill_number=1, directive=0)
        self.skill(servant_number=3, skill_number=2, directive=3)
        self.skill(servant_number=2, skill_number=1, directive=3)
        self.skill(servant_number=2, skill_number=2, directive=0)

        self.master_skill(skill_number=1, directive=0)

        print("turn3 attack")

        self.np_attack(np_number=3)

    def udk_fast(self):
        until_check_png("master_skill")
        until_check_png('attack')
        sleep(1)

        # 1
        print("turn1 skill")

        self.skill(servant_number=1, skill_number=1, directive=0)
        self.skill(servant_number=1, skill_number=2, directive=0)
        self.skill(servant_number=3, skill_number=1, directive=0)
        self.skill(servant_number=3, skill_number=2, directive=0)
        self.skill(servant_number=3, skill_number=3, directive=1)
        self.skill(servant_number=2, skill_number=1, directive=0)
        self.skill(servant_number=2, skill_number=2, directive=1)
        self.skill(servant_number=2, skill_number=3, directive=1)
        self.skill_ex(servant_number=1, skill_number=3, np_type='army')

        print("turn1 attack")

        self.np_attack(np_number=1)

        # 2
        print("turn2 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        print("turn2 attack")

        self.np_attack(np_number=1)

        # 3
        print("turn3 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        print("turn3 attack")

        self.np_attack(np_number=1)

    def bust_3(self):
        until_check_png("master_skill")
        until_check_png('attack')
        sleep(1)

        # 1
        print("turn1 skill")

        # self.skill(servant_number=1, skill_number=1, directive=0)
        # self.skill(servant_number=1, skill_number=2, directive=0)
        self.skill(servant_number=1, skill_number=2, directive=0)
        self.skill(servant_number=2, skill_number=1, directive=0)
        self.skill(servant_number=2, skill_number=2, directive=3)
        # self.skill(servant_number=2, skill_number=3, directive=0)
        self.skill(servant_number=3, skill_number=1, directive=0)
        self.skill(servant_number=3, skill_number=2, directive=0)
        #self.skill(servant_number=3, skill_number=3, directive=0)

        print("turn1 attack")

        self.np_attack(np_number=2)

        # 2
        print("turn2 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        print("turn2 attack")

        # self.skill(servant_number=3, skill_number=3, directive=0)
        self.np_attack(np_number=3)

        # 3
        print("turn3 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        print("turn3 attack")

        self.skill(servant_number=3, skill_number=3, directive=0)
        self.skill(servant_number=1, skill_number=3, directive=0)
        self.np_attack(np_number=1)

    def plapla(self):
        until_check_png("master_skill")
        until_check_png('attack')
        sleep(1)

        # 1
        print("turn1 skill")

        # self.skill(servant_number=1, skill_number=1, directive=0)
        # self.skill(servant_number=1, skill_number=2, directive=0)
        self.skill(servant_number=1, skill_number=3, directive=0)

        # self.skill(servant_number=2, skill_number=1, directive=1)
        # self.skill(servant_number=2, skill_number=2, directive=0)
        # self.skill(servant_number=2, skill_number=3, directive=0)

        # self.skill(servant_number=3, skill_number=1, directive=1)
        # self.skill(servant_number=3, skill_number=2, directive=0)
        # self.skill(servant_number=3, skill_number=3, directive=0)

        # self.master_skill(skill_number=1, directive=1)

        print("turn1 attack")

        self.np_attack(np_number=1)

        # 2
        print("turn2 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        self.skill(servant_number=1, skill_number=1, directive=0)
        self.skill(servant_number=1, skill_number=2, directive=2)
        self.skill(servant_number=1, skill_number=3, directive=3)

        self.skill(servant_number=2, skill_number=1, directive=0)
        self.skill(servant_number=2, skill_number=2, directive=0)
        # self.skill(servant_number=2, skill_number=3, directive=0)

        # self.skill(servant_number=3, skill_number=1, directive=1)
        # self.skill(servant_number=3, skill_number=2, directive=0)
        self.skill(servant_number=3, skill_number=3, directive=0)

        # self.master_skill(skill_number=1, directive=1)

        print("turn2 attack")

        self.np_attack(np_number=[2, 3])

        # 3
        print("turn3 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        # self.skill(servant_number=1, skill_number=1, directive=0)
        # self.skill(servant_number=1, skill_number=2, directive=0)
        # self.skill(servant_number=1, skill_number=3, directive=1)

        self.skill(servant_number=2, skill_number=1, directive=3)
        self.skill(servant_number=2, skill_number=2, directive=3)
        self.skill(servant_number=2, skill_number=3, directive=0)

        self.skill(servant_number=3, skill_number=1, directive=0)
        self.skill(servant_number=3, skill_number=2, directive=3)
        # self.skill(servant_number=3, skill_number=3, directive=0)

        self.master_skill(skill_number=2, directive=3)

        print("turn3 attack")

        self.np_attack(np_number=3)

    def cannon(self):
        until_check_png("master_skill")
        until_check_png('attack')
        sleep(1)

        # 1
        print("turn1 skill")

        self.skill(servant_number=1, skill_number=1, directive=0)
        self.skill(servant_number=1, skill_number=2, directive=0)
        self.skill(servant_number=1, skill_number=3, directive=3)

        self.skill(servant_number=2, skill_number=3, directive=3)

        print("turn1 attack")

        self.np_attack(np_number=3)

        until_check_png("master_skill", clickmid=True)

        # 2
        print("turn2 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        print("turn2 attack")
        self.skill(servant_number=1, skill_number=1, directive=3)
        self.skill(servant_number=1, skill_number=2, directive=0)

        self.skill(servant_number=2, skill_number=1, directive=0)
        self.skill(servant_number=2, skill_number=2, directive=3)

        self.skill(servant_number=3, skill_number=2, directive=0)

        self.np_attack(np_number=3)

        until_check_png("master_skill", clickmid=True)

        # 3
        print("turn3 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        self.skill(servant_number=1, skill_number=1, directive=0)
        self.skill(servant_number=1, skill_number=2, directive=3)

        print("turn3 attack")

        self.np_attack(np_number=3)

    def tanebi_arts(self):
        until_check_png("master_skill")
        until_check_png('attack')
        sleep(1)

        # 1
        print("turn1 skill")

        self.skill(servant_number=1, skill_number=1, directive=0)
        self.skill(servant_number=1, skill_number=2, directive=0)
        self.skill(servant_number=2, skill_number=1, directive=0)
        self.skill(servant_number=2, skill_number=2, directive=2)
        self.skill(servant_number=2, skill_number=3, directive=0)
        self.skill(servant_number=3, skill_number=1, directive=0)
        self.skill(servant_number=3, skill_number=2, directive=1)
        self.skill(servant_number=3, skill_number=3, directive=1)


        print("turn1 attack")

        self.np_attack(np_number=1)

        # 2
        print("turn2 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        print("turn2 attack")

        self.skill(servant_number=1, skill_number=3, directive=0)

        self.np_attack(np_number=1)

        # 3
        print("turn3 skill")
        until_check_png('master_skill', try_time=100, clickmid=False)

        print("turn3 attack")

        self.np_attack(np_number=2)


class Circling(Loop_type):
    def __init__(self, loop_selection, support_mark="any", support_class="mix"):
        super().__init__()
        self.class_select = {
            "all": (px + 202, py + 180),
            "saber": (px + 281, py + 180),
            "archer": (px + 357, py + 180),
            "lancer": (px + 435, py + 180),
            "rider": (px + 513, py + 180),
            "caster": (px + 587, py + 180),
            "assassin": (px + 665, py + 180),
            "berserker": (px + 740, py + 180),
            "extra": (px + 818, py + 180),
            "mix": (px + 892, py + 180)
        }
        self.support_mark = support_mark
        self.loop_type = loop_selection
        self.support_class = support_class

    def loop_frame(self, ap_status=False, cap_apple=3):
        apple = 0
        while True:
            getattr(self, self.loop_type)()
            until_check_png('next', clickmid=True, waiting_time=0.3)
            sleep(1)
            until_click_X('next')
            until_click_X('end')
            until_click_X('continu')

            break_point = False
            t1 = datetime.datetime.now()
            while True:
                print(t1)
                if until_check_png('refresh_list', try_time=1):
                    break
                elif until_check_png('gem', try_time=1):
                    if ap_status == False:
                        break_point = True
                        break
                    else:
                        if apple < cap_apple:
                            if ap_status == "gold":
                                until_click_X("gold_apple", rta=False)
                                until_click_X("accept")
                                apple += 1
                                until_check_png('refresh_list', try_time=1)
                                break
                            elif ap_status == "silver":
                                until_click_X("silver_apple", rta=False)
                                until_click_X("accept")
                                apple += 1
                                until_check_png('refresh_list', try_time=1)
                                break
                            elif ap_status == "gem":
                                until_click_X("gem", rta=False)
                                until_click_X("accept")
                                apple += 1
                                until_check_png('refresh_list', try_time=1)
                                break
                            elif ap_status == "copper":
                                moveTo(px + 910, py + 566)
                                dragTo(px + 910, py + 250, 0.5, button='left')
                                until_click_X("copper_apple", rta=False)
                                until_click_X("accept")
                                apple += 1
                                until_check_png('refresh_list', try_time=1)
                                break
                        else:
                            break_point = True
                            break
            if break_point:
                break

            while True:
                if until_check_png('no_one', try_time=1):
                    until_check_png('refresh_list')
                    until_click_X('refresh_list')
                    until_click_X("hi")
                elif until_check_png('support_on', try_time=1):
                    break

            sleep(0.5)

            click(self.class_select[self.support_class])
            refresh_support = 0
            if self.support_mark != "any":
                while True:
                    try:
                        if locateOnScreen(tp(self.support_mark), confidence=0.9, region=region) is not None:
                            until_click_X(self.support_mark)
                            break
                    except ImageNotFoundException:
                        if refresh_support <= 3:
                            moveTo(px + 1566, py + 800)
                            dragTo(px + 1566, py + 350, 1, button='left')
                            sleep(1)
                            refresh_support += 1
                        else:
                            until_check_png("refresh_list")
                            until_click_X('refresh_list')
                            until_click_X("hi", max_attempts=100)
                            refresh_support = 0
            else:
                until_check_png('support_on')
                click(px + 1820/2, py + 850/2)

# Circling("udk_fast", support_mark="sup_castoria", support_class="caster").loop_frame(ap_status="copper", cap_apple=100)
# Circling("kkr_any", support_mark="sup_NFF", support_class="assassin").loop_frame(ap_status="silver", cap_apple=0)
# Circling("bust_3", support_mark="sand", support_class="mix").loop_frame(ap_status="silver", cap_apple=2)
# Circling("tanebi_arts", support_mark="sup_castoria", support_class="caster").loop_frame(ap_status="gold", cap_apple=0)
# Circling("kkr_fast", support_mark="sup_NFF", support_class="assassin").loop_frame(ap_status="gem", cap_apple=200)


#Circling("odeko", support_mark="sup_castoria", support_class="caster").loop_frame(ap_status="copper", cap_apple=1)

#Circling("plapla", support_mark="sup_castoria", support_class="caster").loop_frame(ap_status="gem", cap_apple=0)
