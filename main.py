import pygame
import random

WIDTH = 600
HEIGHT = 500

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT))
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
    pygame.quit()
