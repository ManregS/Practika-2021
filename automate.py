import pygame as pg
import random
from car import *

pg.init()
screen = pg.display.set_mode((1400, 800))
BACKGROUND = pg.image.load("src\\Автомат.png")
COLOR_INACTIVE = pg.Color('green')
COLOR_ACTIVE = pg.Color('red')
COLOR_BLACK = pg.Color('black')
FONT = pg.font.SysFont("Arial", 50)
FUEL_INFO = {"92": 44.44,
             "95": 47.90,
             "98": 54.88}
K_NUMBERS = [pg.K_PERIOD, pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]


class Text:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_BLACK
        self.text = text
        self.txt_surface = FONT.render(self.text, True, COLOR_BLACK)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 2)
        if "\n" not in self.text:
            screen.blit(self.txt_surface, (self.rect.x + (self.rect.w / 2 - self.txt_surface.get_width() / 2), self.rect.y + (self.rect.h / 2 - self.txt_surface.get_height() / 2)))
        else:
            message = self.text.split("\n")
            for i in range(len(message)):
                if self.text.count("\n") > 3:
                    txt = pg.font.SysFont("Arial", 40).render(message[i], True, COLOR_BLACK)
                else:
                    txt = FONT.render(message[i], True, COLOR_BLACK)
                message[i] = txt
                if i == 0:
                    if self.text.count("\n") > 1:
                        screen.blit(txt, (self.rect.x + (self.rect.w / 2 - txt.get_width() / 2), self.rect.y))
                    else:
                        screen.blit(txt, (self.rect.x + 5, self.rect.y))
                else:
                    screen.blit(txt, (self.rect.x + 5, self.rect.y + ((message[i - 1].get_height()) * i)))
    
    def Clear(self):
        self.text = ""
        self.txt_surface = FONT.render("", True, COLOR_BLACK)


class Button:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(self.text, True, COLOR_BLACK)
        self.active = False

    def draw(self, screen, outline=None):
        if outline:
            pg.draw.rect(screen, outline, (self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4), 0)
        pg.draw.rect(screen, self.color, self.rect, 0)
        screen.blit(self.txt_surface, (self.rect.x + (self.rect.w / 2 - self.txt_surface.get_width() / 2), self.rect.y + (self.rect.h / 2 - self.txt_surface.get_height() / 2)))

    def makeActive(self, pos):
        if self.rect.collidepoint(pos):
            for el in el_list:
                el.active = False
                el.color = COLOR_INACTIVE
            self.active = True
            self.color = COLOR_ACTIVE
            return True
        return False


class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(self.text, True, COLOR_BLACK)
        self.active = False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + (self.rect.w / 2 - self.txt_surface.get_width() / 2), self.rect.y + (self.rect.h / 2 - self.txt_surface.get_height() / 2)))
        pg.draw.rect(screen, self.color, self.rect, 2)

    def makeActive(self, pos):
        if self.rect.collidepoint(pos):
            self.active = True
            self.color = COLOR_ACTIVE
        else:
            self.active = False
            self.color = COLOR_INACTIVE

    def inputValue(self, event):
        if self.active:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            if (event.key == K_NUMBERS[0]) and (self.txt_surface.get_width() < self.rect.w):
                if (len(self.text) > 0) and ("." not in self.text):
                    self.text += event.unicode
            elif (event.key in K_NUMBERS[1:]) and (self.txt_surface.get_width() < self.rect.w):
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, COLOR_BLACK)

    def Clear(self):
        self.text = ""
        self.txt_surface = FONT.render("", True, COLOR_BLACK)


class Card:
    def __init__(self, x, y, w, h, card):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.card = card
        self.active = False
    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
        screen.blit(self.card, (self.rect.x + (self.rect.w / 2 - self.card.get_width() / 2), self.rect.y + (self.rect.h / 2 - self.card.get_height() / 2)))

    def makeActive(self, pos):
        if self.rect.collidepoint(pos):
            self.active = True
            self.color = COLOR_ACTIVE
            return True
        elif buttonPay.rect.collidepoint(pos):
            self.active = self.active
            self.color = self.color
        else:
            self.active = False
            self.color = COLOR_INACTIVE
            return False


class Automate:
    def __init__(self, fuel_type="", liters=""):
        self.fuel_type = fuel_type
        self.liters = liters

    def check(self, car: Car):
        if self.fuel_type == "":
            return "Select fuel type\n", 0
        if self.liters == "" or float(self.liters) == 0.0:
            return "Liters is empty\n", 0
        if self.fuel_type != car.fuel:
            return "This fuel does not\nfit your car", 0
        if (car.count_of_gasoline + float(self.liters)) > car.max_gasoline:
            return "So many liters will\nnot fit in your tank", 0
        if (self.liters * FUEL_INFO[car.fuel]) > car.count_of_money:
            return "Not enough money\nto pay", 0
        else:
            car.count_of_gasoline += float(self.liters)
            car.count_of_money -= self.liters * FUEL_INFO[car.fuel]
            return "Payment passed\nCar tank: " + str(round(car.count_of_gasoline, 2)) + " liters\nYour balance: " + str(round(car.count_of_money, 2)), 1

    def Clear(self):
        self.fuel_type = ""
        self.liters = ""


def Screen(car_fuel_type, car_liters, car_liters_MAX, money):
    text_car_info.text = ("Car Info\n" + ("Fuel type: "+str(car_fuel_type)+"\n") + ("Tank: "+str(round(car_liters, 2))+" liters\n") + ("MAX: "+str(car_liters_MAX)+" liters\n") + ("Card: "+str(round(money, 2))+" rub"))
    screen.fill((255, 255, 255))
    screen.blit(BACKGROUND, (370, 0))
    card.draw(screen)
    for text in text_list:
        text.draw(screen)
    for el in el_list:
        if el in el_list[:-1]:
            el.draw(screen, COLOR_BLACK)
        else:
            el.draw(screen)
    buttonPay.color = COLOR_INACTIVE
    buttonPay.active = False
    pg.display.update()

def Pay(automate: Automate, inputbox: InputBox, text: Text, car: Car):
    click_pay = 0
    if inputbox.text != "":
        automate.liters = float(inputbox.text)
    message, click_pay = automate.check(car)
    text.text = message
    inputbox.Clear()
    automate.Clear()
    return click_pay

def Exit(text: Text, pay: Button, exit: Button):
    text.text = "Instruction\n1.Choose fuel type\n2.Enter number of liters\n3.Choose your card and pay\n"
    pay.color = COLOR_INACTIVE
    pay.active = False
    exit.color = COLOR_INACTIVE
    exit.active = False

cards = [pg.image.load("src\\cards\\card" + str(i) + ".png") for i in range(1, 4)]
card = Card(10, 300, 310, 200, cards[random.randint(0, 2)])
button92 = Button(485, 45, 126, 100, "92")
button95 = Button(637, 45, 126, 100, "95")
button98 = Button(789, 45, 126, 100, "98")
inputbox = InputBox(485, 235, 430, 100)
buttonPay = Button(665, 550, 250, 80, "Pay by card")
buttonExit = Button(487, 550, 150, 80, "Exit")
text_result = Text(485, 340, 430, 200, ("Instruction\n1.Choose fuel type\n2.Enter number of liters\n3.Choose your card and pay\n"))
text_fuel_info = Text(1040, 10, 350, 250, ("Fuel Info\n" + ("92: " + str(FUEL_INFO["92"])) + " rub\n" + ("95: " + str(FUEL_INFO["95"])) + " rub\n" + ("98: " + str(FUEL_INFO["98"])) + " rub"))
text_car_info = Text(10, 10, 350, 250)
el_list = [button92, button95, button98, buttonPay, buttonExit, inputbox]
text_list = [text_result, text_fuel_info, text_car_info]
