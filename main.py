import random
import time
import threading

import pygame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
import sqlite3

import Data
import UI

WIDTH = 863
HEIGHT = 503

bg_menu = pygame.image.load("Source/Main_Menu.png")
bg_ingame = pygame.image.load("Source/GAME_UI.png")
driver: webdriver.Firefox | None = None

class ProgressBarColor:
    __slots__ = ("__progress", "__colors")
    __obj = None
    def __new__(cls, progress: int = 0):
        if cls.__obj is None:
            cls.__obj = super(ProgressBarColor, cls).__new__(cls)
        return cls.__obj

    def __init__(self):
        self.__progress = 0
        self.__colors = [255, 0, 0]

    def update(self, progress: int):
        if progress == self.__progress:
            return
        diff = abs(progress - self.__progress)
        color_change = int(255 / 100 * diff)
        if progress > self.__progress:
            self.__colors[0] = max(0, self.__colors[0] - color_change)
            self.__colors[1] = min(255, self.__colors[1] + color_change)
        else:
            self.__colors[0] = min(255, self.__colors[0] + color_change)
            self.__colors[1] = max(0, self.__colors[1] - color_change)
        self.__progress = progress

    @property
    def colors(self):
        return self.__colors


def music_on():
    try:
        global driver
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options = options)
        driver.get("https://lofiradio.ru/")
        driver.find_element(By.ID, "vidio_toggle").click()
        driver.find_element(By.ID, "lunaradiobuttonvolumeoff").click()
        move = ActionChains(driver)
        thumb = driver.find_element(By.ID, "lunaradiovolumegrab")
        driver.find_element(By.ID, "lunaradiobuttonplay").click()
        for position in range(0, 100 + 1, 5):
            move.click_and_hold(thumb).move_by_offset(20, 0).release().perform()
            time.sleep(0.1)
        # while True:
        #     pass
    except:
        pass


def start_menu(screen):
    game_running = True
    start_butt = UI.Button(210, 70, 30, 400)
    while game_running:
        screen.blit(bg_menu, (0, 0))
        start_butt.draw_start(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
        pygame.display.update()

def start_game(screen):
    con = sqlite3.connect("DATABASE.db")
    cur = con.cursor()
    res = cur.execute("SELECT fish_pool, price_pool FROM Inventory WHERE Player_ID='1'").fetchone()
    game_running = True
    is_fishing = False
    fish_founded = False
    fishing_butt = UI.Button(200, 70, 240, 380, butt=pygame.image.load("Source/Button.png"))
    infishing_butt = UI.Button(200, 70, 240, 380, butt=pygame.image.load("Source/Stop Button.png"))
    sell_butt = UI.Button(123, 30, 727, 465)
    up_hook_butt = UI.Button(140, 50, 30, 370)
    up_rod_butt = UI.Button(140, 50, 30, 306)
    bg_butt = UI.Button(260, 30, 375, 470)
    achivs_display = UI.Button(168, 26, 212, 2)
    timer = 0
    last_time = 0
    fishing_window = pygame.image.load("Source/Fishing Window.png")
    fish = pygame.transform.scale(pygame.image.load("Source/Fish.png"), (45, 20))
    fish_pos = (0, 0)
    movement_x = 0
    movement_y = 0
    mouse = UI.Mouse(pygame.mouse)
    current_fishing_rod = cur.execute("SELECT rod FROM Inventory WHERE Player_ID='1'").fetchone()[0]
    current_hook = cur.execute("SELECT hook FROM Inventory WHERE Player_ID='1'").fetchone()[0]
    fishing_progress = 0
    sell_price = 0
    money = cur.execute("SELECT money FROM Inventory WHERE Player_ID='1'").fetchone()[0]
    fishes = []
    fishes_for_draw = []
    achivs = cur.execute("SELECT achiv FROM Inventory WHERE Player_ID='1'").fetchone()[0].split(',')
    background = 0
    if res[0] != "" or res[0] is not None:
        for i in range(len(res[0].split(",")) - 1):
            fishes.append([res[0].split(",")[i], res[1].split(",")[i]])
            fishes_for_draw.append(pygame.transform.scale(pygame.image.load(Data.fishes[int(res[0].split(",")[i])]),
                                   (104, 39)))
            sell_price += int(res[1].split(",")[i])
    while game_running:
        screen.blit(bg_ingame, (0, 0))
        screen.blit(Data.backgrounds[background % len(Data.backgrounds)], (214, 38))
        screen.blit(Data.fishing_rods[current_fishing_rod % len(Data.fishing_rods)], (25, 24))
        screen.blit(Data.hooks[current_hook % len(Data.fishing_rods)], (25, 146))
        UI.print_text(screen, str(sell_price), 805, 434, 25, [255, 244, 0])
        UI.print_text(screen, str(money), 115, 280, 20, [0, 0, 0])
        UI.print_text(screen, str(current_fishing_rod), 88, 355, 13, [0, 0, 0])
        UI.print_text(screen, str(current_hook), 88, 418, 13, [0, 0, 0])
        achivs_display.show_achiv(screen)
        for i in range(len(achivs)):
            pygame.draw.rect(screen, [0, 0, 0], [212 + 28 * i, 2, 26, 26], 2)
            if achivs[i] == "1":
                pygame.draw.line(screen, [0, 255, 0], (212 + 28 * i, 10), (224 + 28 * i, 26), 3)
                pygame.draw.line(screen, [0, 255, 0], (224 + 28 * i, 26), (239 + 28 * i, 2), 3)
        if bg_butt.change_bg():
            background += 1
        if sell_butt.sell(cur, sell_price):
            fishes = []
            fishes_for_draw = []
            money += sell_price
            sell_price = 0
        if up_rod_butt.up_rod(cur):
            achivs[2] = "1"
            cur.execute("UPDATE Inventory SET achiv = '{}' WHERE Player_ID = '1'".format(",".join(achivs)))
            money -= 100
            current_fishing_rod += 1
        if up_hook_butt.up_hook(cur):
            achivs[3] = "1"
            cur.execute("UPDATE Inventory SET achiv = '{}' WHERE Player_ID = '1'".format(",".join(achivs)))
            money -= 100
            current_hook += 1
        x = 21
        for i in fishes_for_draw:
            screen.blit(i, (736, x))
            x += 61.5
        if not is_fishing:
            fish_founded = False
            if len(fishes) < 7:
                is_fishing = fishing_butt.draw_fishing(screen)
            else:
                achivs[1] = "1"
                cur.execute("UPDATE Inventory SET achiv = '{}' WHERE Player_ID = '1'".format(",".join(achivs)))
            if is_fishing:
                timer = time.time()
        else:
            is_fishing = not infishing_butt.draw_fishing(screen)
            if not is_fishing and fish_founded:
                achivs[5] = "1"
                cur.execute("UPDATE Inventory SET achiv = '{}' WHERE Player_ID = '1'".format(",".join(achivs)))
            #гэмблинг на поимку с шансом, увеличивающимся каждую секунду
            if not fish_founded and random.randint(0, 100) > 100 - (time.time() - timer) - current_hook * 8 and int(last_time) < int(time.time()):
                fish_founded = True
                fishing_progress = 0
            if fish_founded:
                pb_color = ProgressBarColor()
                screen.blit(fishing_window, (250, 50))
                if int(last_time) < int(time.time()):
                    movement_y = random.randint(-2, 2)
                    movement_x = random.randint(-2, 2)
                if int(last_time / 0.02) < int(time.time() / 0.02):
                    fish_pos = ((fish_pos[0] + movement_x) % 375, (fish_pos[1] + movement_y) % 300)
                screen.blit(fish, (fish_pos[0] + 255, fish_pos[1] + 55))
                if mouse.fishing(screen, 30 + 10 * current_fishing_rod, (fish_pos[0] + 277, fish_pos[1] + 65)):
                    if int(last_time / 0.02) < int(time.time() / 0.02):
                        fishing_progress += 1
                elif fishing_progress > 0:
                    if int(last_time / 0.02) < int(time.time() / 0.02):
                        fishing_progress -= 1
                pb_color.update(fishing_progress)
                pygame.draw.rect(screen, pb_color.colors, [450, 390, 240 * (fishing_progress / 100), 60])
                pygame.draw.rect(screen, [255, 127, 39], [450, 390, 240, 60], 3)
                if fishing_progress >= 100:
                    achivs[0] = "1"
                    cur.execute("UPDATE Inventory SET achiv = '{}' WHERE Player_ID = '1'".format(",".join(achivs)))
                    is_fishing = False
                    infishing_butt.flag = False
                    fishing_butt.flag = True
                    z1 = random.randint(0, len(Data.fishes) - 1)
                    if z1 == 2:
                        achivs[4] = "1"
                        cur.execute("UPDATE Inventory SET achiv = '{}' WHERE Player_ID = '1'".format(",".join(achivs)))
                    z2 = random.randint(15, 30)
                    fishes.append([z1, z2])
                    sell_price += z2
                    fishes_for_draw.append(pygame.transform.scale(pygame.image.load(Data.fishes[z1]), (104, 39)))
                    ans = ''
                    ans2 = ''
                    for i, j in fishes:
                        ans = ans + str(i) + ','
                        ans2 = ans2 + str(j) + ','
                    cur.execute("UPDATE Inventory SET fish_pool = '{}' WHERE Player_ID = '1'".format(ans))
                    cur.execute("UPDATE Inventory SET price_pool = '{}' WHERE Player_ID = '1'".format(ans2))
            last_time = time.time()
        con.commit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                con.commit()
                con.close()
                game_running = False
        pygame.display.update()
    return


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ялбалык")
    t2 = threading.Thread(target = music_on, daemon = True)
    t2.start()
    start_menu(screen)
    pygame.quit()
    if isinstance(driver, webdriver.Firefox):
        driver.quit()
