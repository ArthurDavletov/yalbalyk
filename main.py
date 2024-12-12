import pygame
import UI
import random

WIDTH = 863
HEIGHT = 503

bg_menu = pygame.image.load("Source/Main_Menu.png")
bg_ingame = pygame.image.load("Source/GAME_UI.png")


def start_menu(screen):
    game_running = True
    start_butt = UI.Button(210, 70, 30, 400)
    while game_running:
        for event in pygame.event.get():
            screen.blit(bg_menu, (0, 0))
            start_butt.draw_start(screen)
            if event.type == pygame.QUIT:
                game_running = False
            pygame.display.update()
    return


def start_game(screen):
    game_running = True
    while game_running:
        for event in pygame.event.get():
            screen.blit(bg_ingame, (0, 0))
            if event.type == pygame.QUIT:
                game_running = False
            pygame.display.update()
    return

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start_menu(screen)
    pygame.quit()
