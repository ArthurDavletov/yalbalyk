import pygame
import UI
import random
import time

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
    game_running = True
    is_fishing = False
    fish_founded = False
    fishing_butt = UI.Button(200, 70, 240, 380, butt=pygame.image.load("Source/Button.png"))
    infishing_butt = UI.Button(200, 70, 240, 380, butt=pygame.image.load("Source/Stop Button.png"))
    timer = 0
    last_time = 0
    fishing_window = pygame.image.load("Source/Fishing Window.png")
    while game_running:
        screen.blit(bg_ingame, (0, 0))
        if not is_fishing:
            fish_founded = False
            is_fishing = fishing_butt.draw_fishing(screen)
            if is_fishing:
                timer = time.time()
        else:
            #гэмблинг на поимку с шансом, увеличивающимся каждую секунду
            if not fish_founded and random.randint(0, 100) > 100 - (time.time() - timer) and int(last_time) < int(time.time()):
                fish_founded = True
            if fish_founded:
                screen.blit(fishing_window, (250, 50))
            is_fishing = not infishing_butt.draw_fishing(screen)
            last_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
        pygame.display.update()
    return


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start_menu(screen)
    pygame.quit()
