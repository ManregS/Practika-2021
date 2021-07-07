import pygame
from pygame.locals import *
import random

# инициализация модуля pygame
pygame.init()

# создание заднего поля нашей игры
width_win = 1400
height_win = 800
win = pygame.display.set_mode((width_win, height_win))

cards = [pygame.image.load("src\\cards\\card" + str(i) + ".png") for i in range(1, 4)]

class Card:
    def __init__(self, width, height, money, card):
        self.width = width
        self.height = height
        self.money = money
        self.card = card
        self.active_color = pygame.Color('red')
        self.inactive_color = pygame.Color('green')
        self.click_on = False

    def draw(self, x, y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(win, self.active_color, (x - 3, y - 3, self.width + 6, self.height + 6))
            win.blit(self.card, (x, y))

            if click[0] == 1:
                self.click_on = True
                if self.click_on == True:
                    pygame.draw.rect(win, self.active_color, (x - 3, y - 3, self.width + 6, self.height + 6))
                    win.blit(self.card, (x, y))
        else:
            if self.click_on == False:
                pygame.draw.rect(win, self.inactive_color, (x - 3, y - 3, self.width + 6, self.height + 6))
                win.blit(self.card, (x, y))


run = True
card = Card(300, 190, 1000, cards[random.randint(0, 2)])
x = width_win - 310
y = height_win - 200
while run:

    card.draw(x, y)
    win.blit(card.card, (x, y))

    for motion in pygame.event.get():
        if motion.type == pygame.QUIT:
            run = False

    pygame.time.delay(50)
    # обновление дисплея
    pygame.display.update()

# выход из открывшего окна игры
pygame.quit()