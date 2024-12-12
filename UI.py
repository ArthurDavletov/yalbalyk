import pygame
import main


#butt = pygame.image.load("butt_pic.png")
#butt_pres = pygame.image.load("butt_clicked.png")
# ВСЕ, ЧТО ЗАКОММЕНЧЕНО, НУЖНО НА СЛУЧАЙ, ЕСЛИ КНОПКУ НАДО БУДЕТ ОТРИСОВЫВАТЬ


def print_text(screen, message, x, y, font_size, font_color=(0, 0, 0), font_type="Palatino Linotype.ttf"):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button:
    def __init__(self, width, height, x, y, message='', x_m=0, y_m=0, font=20, font_color=(0, 0, 0)):
        self.font_color = font_color
        self.width = width
        self.height = height
        #self.act_cl = butt
        #self.inact_cl = butt_pres
        self.message = message
        self.x = x
        self.y = y
        self.x_m = x_m
        self.y_m = y_m
        self.font = font

    def draw_start(self, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            #cache = pygame.transform.scale(butt_pres, (self.width, self.height))
            #screen.blit(cache, (self.x, self.y))
            if click[0] == 1:
                main.start_game(screen)
        #else:
            #cache = pygame.transform.scale(butt, (self.width, self.height))
            #screen.blit(cache, (self.x, self.y))
        #print_text(screen, self.message, self.x_m, self.y_m, self.font, self.font_color)
