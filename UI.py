import math

import pygame

import Data
import main


# ВСЕ, ЧТО ЗАКОММЕНЧЕНО, НУЖНО НА СЛУЧАЙ, ЕСЛИ КНОПКУ НАДО БУДЕТ ОТРИСОВЫВАТЬ


def print_text(screen, message, x, y, font_size, font_color=(0, 0, 0), font_type="arial"):
    font_type = pygame.font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Mouse:
    def __init__(self, mouse):
        self.mouse = mouse

    def fishing(self, screen, fishing_road, fish_pos):
        mouse_pos = self.mouse.get_pos()
        if 250 < mouse_pos[0] < 680 and 50 < mouse_pos[1] < 380:
            pygame.draw.circle(screen, color="White", center=self.mouse.get_pos(), radius=fishing_road, width=4)
            if math.sqrt((mouse_pos[0] - fish_pos[0]) ** 2 + (mouse_pos[1] - fish_pos[1]) ** 2) <= fishing_road:
                return True
            return False


class Button:
    def __init__(self, width, height, x, y, butt=0, message='', x_m=0, y_m=0, font=20, font_color=(0, 0, 0)):
        self.font_color = font_color
        self.width = width
        self.height = height
        self.message = message
        self.x = x
        self.y = y
        self.x_m = x_m
        self.y_m = y_m
        self.font = font
        self.flag = False
        if butt != 0:
            self.button = pygame.transform.scale(butt, (self.width, self.height))

    def draw_start(self, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            if click[0] == 1:
                main.start_game(screen)

    def sell(self, cur, price):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            if click[0] == 1:
                money = cur.execute("SELECT money FROM Inventory WHERE Player_ID='1'").fetchone()[0]
                cur.execute("UPDATE Inventory SET money = '{}' WHERE Player_ID = '1'".format(money + price))
                cur.execute("UPDATE Inventory SET fish_pool = '' WHERE Player_ID = '1'")
                cur.execute("UPDATE Inventory SET price_pool = '' WHERE Player_ID = '1'")
                return True
        return False

    def draw_fishing(self, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        screen.blit(self.button, (self.x, self.y))
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            if click[0] == 1 and self.flag:
                self.flag = False
                return True
        else:
            self.flag = True
        return False

    def up_hook(self, cur):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            if click[0] == 1 and self.flag:
                self.flag = False
                money = cur.execute("SELECT money FROM Inventory WHERE Player_ID='1'").fetchone()[0]
                if money < 100:
                    return False
                cur.execute("UPDATE Inventory SET money = '{}' WHERE Player_ID = '1'".format(money - 100))
                hook = cur.execute("SELECT hook FROM Inventory WHERE Player_ID='1'").fetchone()[0]
                cur.execute("UPDATE Inventory SET hook = '{}' WHERE Player_ID = '1'".format(hook + 1))
                return True
        else:
            self.flag = True
        return False

    def up_rod(self, cur):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            if click[0] == 1 and self.flag:
                self.flag = False
                money = cur.execute("SELECT money FROM Inventory WHERE Player_ID='1'").fetchone()[0]
                if money < 100:
                    return False
                cur.execute("UPDATE Inventory SET money = '{}' WHERE Player_ID = '1'".format(money - 100))
                rod = cur.execute("SELECT rod FROM Inventory WHERE Player_ID='1'").fetchone()[0]
                cur.execute("UPDATE Inventory SET rod = '{}' WHERE Player_ID = '1'".format(rod + 1))
                return True
        else:
            self.flag = True
        return False

    def change_bg(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            if click[0] == 1 and self.flag:
                self.flag = False
                return True
        else:
            self.flag = True
        return False

    def show_achiv(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.x <= int(mouse[0]) <= int(self.x + self.width - 5) and self.y < int(mouse[1]) < self.y + self.height:
            print_text(screen, Data.achivs[int((mouse[0] - self.x) / (self.width / len(Data.achivs)))], 420, 5, 15)