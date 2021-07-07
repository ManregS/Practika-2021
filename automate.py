import pygame as pg

pg.init()
screen = pg.display.set_mode((1400, 800))
BACKGROUND = pg.image.load("src\\Автомат.png")
COLOR_INACTIVE = pg.Color('green')
COLOR_ACTIVE = pg.Color('red')
COLOR_BLACK = pg.Color('black')
FONT = pg.font.SysFont("Arial", 50)
FUEL_INFO = { "92": 44.44, 
              "95": 47.90, 
              "98": 54.88 }
K_NUMBERS = [pg.K_PERIOD, pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]


class Text:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_BLACK
        self.text = text
        self.txt_surface = FONT.render(self.text, True, COLOR_BLACK)

    def draw(self, screen, outline=True):
        screen.blit(self.txt_surface, (self.rect.x + (self.rect.w/2 - self.txt_surface.get_width()/2), self.rect.y + (self.rect.h/2 - self.txt_surface.get_height()/2)))
        if outline:
            pg.draw.rect(screen, outline, self.rect, 2)
        else:
            FONT = pg.font.SysFont("Arial", 35)
            self.txt_surface = FONT.render(self.text, True, COLOR_BLACK)

    def printValue(self, value):
        FONT = pg.font.SysFont("Arial", 40)
        self.txt_surface = FONT.render(str(value), True, COLOR_BLACK)


class Button:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(self.text, True, COLOR_BLACK)
        self.active = False

    def draw(self, screen, outline=None):
        if outline:
            pg.draw.rect(screen, outline, (self.rect.x-2, self.rect.y-2, self.rect.width+4, self.rect.height+4), 0)
        pg.draw.rect(screen, self.color, self.rect, 0)
        screen.blit(self.txt_surface, (self.rect.x + (self.rect.w/2 - self.txt_surface.get_width()/2), self.rect.y + (self.rect.h/2 - self.txt_surface.get_height()/2)))

    def makeActive(self, pos):
        if self.rect.collidepoint(pos):
            self.active = True
            for button in auto_list:
                button.color = COLOR_INACTIVE
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
        screen.blit(self.txt_surface, (self.rect.x + (self.rect.w/2 - self.txt_surface.get_width()/2), self.rect.y + (self.rect.h/2 - self.txt_surface.get_height()/2)))
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


class Automate:
    def __init__(self, fuel_type="", liters=0.0, money=0):
        self.fuel_type = fuel_type
        self.liters = liters
        self.money = money

    def check(self, car_fuel_type, car_liters, car_liters_MAX):
        if self.fuel_type == "":
            return "Select fuel type"
        if self.fuel_type != car_fuel_type:
            return "This fuel does not fit your car"
        if (car_liters + float(self.liters)) > car_liters_MAX:
            return "So many liters will not fit in your tank"
        if (car_liters * FUEL_INFO[car_fuel_type]) > self.money:
            return "Not enough money to pay"
        else:
            return car_liters + float(self.liters) , self.money - (self.liters * FUEL_INFO[car_fuel_type])
    
    def Clear(self):
        self.fuel_type = ""
        self.liters = ""


def Screen():
    screen.fill((255, 255, 255))
    screen.blit(BACKGROUND, (370, 0))
    text_result.draw(screen)
    text_fuel_info.draw(screen, False)
    for button in auto_list:
        if button in auto_list[:-1]:
            button.draw(screen, COLOR_BLACK)
        else:
            button.draw(screen)
    pg.display.update()

def Pay(automate: Automate, inputbox: InputBox, text: Text, car_fuel_type, car_liters, car_liters_MAX):
    if inputbox.text != "":
        automate.liters = float(inputbox.text)
    result = automate.check(car_fuel_type, car_liters, car_liters_MAX)
    text.printValue(result)
    inputbox.Clear()
    automate.Clear()

button92 = Button(485, 45, 126, 100, "92")
button95 = Button(637, 45, 126, 100, "95")
button98 = Button(789, 45, 126, 100, "98")
inputbox = InputBox(485, 235, 430, 100)
buttonPay = Button(665, 550, 250, 80, "Pay by card")
buttonExit = Button(20, 700, 150, 80, "Exit")
text_result = Text(485, 340, 430, 200)
text_fuel_info = Text(1200, 10, 200, 200, str(FUEL_INFO))
#text_car_info = Text()
auto_list = [button92, button95, button98, buttonPay, buttonExit, inputbox]