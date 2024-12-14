import random
import time

import pygame
import sqlite3

import Data
import UI

WIDTH = 863
HEIGHT = 503

bg_menu = pygame.image.load("Source/Main_Menu.png")
bg_ingame = pygame.image.load("Source/GAME_UI.png")


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
    return


def start_game(screen):
    con = sqlite3.connect("DATABASE.db")
    cur = con.cursor()
    res = cur.execute("SELECT fish_pool, price_pool FROM Inventory WHERE Player_ID='1'").fetchone()
    game_running = True
    is_fishing = False
    fish_founded = False
    fishing_butt = UI.Button(200, 70, 240, 380, butt=pygame.image.load("Source/Button.png"))
    infishing_butt = UI.Button(200, 70, 240, 380, butt=pygame.image.load("Source/Stop Button.png"))
    timer = 0
    last_time = 0
    fishing_window = pygame.image.load("Source/Fishing Window.png")
    fish = pygame.transform.scale(pygame.image.load("Source/Fish.png"), (45, 20))
    fish_pos = (0, 0)
    movement_x = 0
    movement_y = 0
    mouse = UI.Mouse(pygame.mouse)
    current_fishing_road = 1
    current_hook = 0
    fishing_progress = 0
    fishes = []
    fishes_for_draw = []
    if res[0] != "":
        for i in range(len(res[0].split(",")) - 1):
            fishes.append([res[0].split(",")[i], res[1].split(",")[i]])
            fishes_for_draw.append(pygame.transform.scale(pygame.image.load(Data.fishes[int(res[0].split(",")[i])]),
                                   (104, 39)))
    while game_running:
        screen.blit(bg_ingame, (0, 0))
        screen.blit(Data.fishing_roads[current_fishing_road], (25, 24))
        screen.blit(Data.hooks[current_hook], (25, 146))
        x = 21
        for i in fishes_for_draw:
            screen.blit(i, (736, x))
            x += 61.5
        if not is_fishing:
            fish_founded = False
            if len(fishes) < 7:
                is_fishing = fishing_butt.draw_fishing(screen)
            if is_fishing:
                timer = time.time()
        else:
            is_fishing = not infishing_butt.draw_fishing(screen)
            #гэмблинг на поимку с шансом, увеличивающимся каждую секунду
            if not fish_founded and random.randint(0, 100) > 10 - (time.time() - timer) and int(last_time) < int(time.time()):
                fish_founded = True
                fishing_progress = 0
            if fish_founded:
                screen.blit(fishing_window, (250, 50))
                if int(last_time) < int(time.time()):
                    movement_y = random.randint(-2 + current_hook, 2 - current_hook)
                    movement_x = random.randint(-2 + current_hook, 2 - current_hook)
                if int(last_time / 0.02) < int(time.time() / 0.02):
                    fish_pos = ((fish_pos[0] + movement_x) % 375, (fish_pos[1] + movement_y) % 300)
                screen.blit(fish, (fish_pos[0] + 255, fish_pos[1] + 55))
                if mouse.fishing(screen, 30 + 10 * current_fishing_road, (fish_pos[0] + 277, fish_pos[1] + 65)):
                    if int(last_time / 0.02) < int(time.time() / 0.02):
                        fishing_progress += 1
                elif fishing_progress > 0:
                    if int(last_time / 0.02) < int(time.time() / 0.02):
                        fishing_progress -= 1
                pygame.draw.rect(screen, [255, 201, 14], [450, 390, 240 * (fishing_progress / 100), 60])
                pygame.draw.rect(screen, [255, 127, 39], [450, 390, 240, 60], 3)
                if fishing_progress >= 100:
                    is_fishing = False
                    infishing_butt.flag = False
                    fishing_butt.flag = True
                    z = random.randint(0, len(Data.fishes) - 1)
                    fishes.append([z, random.randint(15, 30)])
                    fishes_for_draw.append(pygame.transform.scale(pygame.image.load(Data.fishes[z]), (104, 39)))
                    ans = ''
                    ans2 = ''
                    for i, j in fishes:
                        ans = ans + str(i) + ','
                        ans2 = ans2 + str(j) + ','
                    cur.execute("UPDATE Inventory SET fish_pool = '{}' WHERE Player_ID = '1'".format(ans))
                    cur.execute("UPDATE Inventory SET price_pool = '{}' WHERE Player_ID = '1'".format(ans2))
                last_time = time.time()
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
    start_menu(screen)
    pygame.quit()
