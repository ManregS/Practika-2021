import pygame
from pygame.locals import *
import car
import time
import random
from automate import *

pygame.mixer.pre_init(44100, -16, 1, 512)

pygame.init()

width_win = 1400
height_win = 800
win = pygame.display.set_mode((width_win, height_win))

pygame.display.set_caption("Car Game")

def print_text(message, x, y, font_color, font_size, font_type = "src\\Printer.ttf"):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))

def exit():
    pygame.quit()

def go():
    run_game = True
    while run_game == True:
        run_game = main()


class Menu_Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (163, 163, 40)
        self.active_color = (254, 254, 3)

    def draw(self, x, y, message, action):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(win, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(win, self.inactive_color, (x, y, self.width, self.height))
        print_text(message, x + 7, y + 13.5, (0, 0, 0), 50)


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (163, 163, 40)
        self.active_color = (254, 254, 3)
        self.click_on = None
        self.check_on = False

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(win, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                self.click_on = True
                self.check_on = True
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(win, self.inactive_color, (x, y, self.width, self.height))
        print_text(message, x + 7, y + 13.5, (0, 0, 0), 50)


def main():
    pygame.mixer.music.load("src\\fon_music_2.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)

    first_car_sound = pygame.mixer.Sound("src\\first_car_sound.ogg")
    gasoline_sound = pygame.mixer.Sound("src\\gasoline.ogg")
    second_car_sound = pygame.mixer.Sound("src\\second_car_sound.ogg")

    bg = pygame.image.load("src\\bg.jpg")

    rand = random.randint(1, 2)
    rand_2 = random.randint(1, 5)
    if rand == 1:
        image = pygame.image.load("src\\first_car\\car" + str(rand_2) + ".png")
        kols = [pygame.image.load("src\\first_car\\kol_" + str(i) + ".png") for i in range(1, 9)]
        x_kol_1 = y_kol_1 = x_kol_2 = y_kol_2 = 0
    else:
        image = pygame.image.load("src\\second_car\\car" + str(rand_2) + ".png")
        kols = [pygame.image.load("src\\second_car\\kol_" + str(i) + ".png") for i in range(1, 9)]
        x_kol_1 = -7
        y_kol_1 = 8
        x_kol_2 = 2
        y_kol_2 = 8

    count = i = 0
    check_sound_1 = check_sound_2 = check_sound_3 = check_car_position = True
    check_exit = False

    next_button = Button(220, 80)
    run = True
    array_fuel = ["92", "95", "98"]
    while run:
        win.blit(bg, (0, 0))

        i += 1
        if i == 8:
            i = 0
        if next_button.check_on == False:
            next_button.draw(width_win - 270, height_win - 130, "NEXT CAR")

        if next_button.click_on == True:
            if check_car_position == True:
                next_car = car.Car(random.randint(0, 2500), random.randint(60, 120), random.randint(5, 50), image, 20, 350, array_fuel[random.randint(0, 2)])
                check_car_position = False

            if check_sound_1 == True:
                first_car_sound.play().set_volume(0.25)
                check_sound_1 = False

            if -(next_car.width + next_car.speed * 3) + next_car.speed * count < width_win:
                x = -(next_car.width + next_car.speed * 3) + next_car.speed * count
                y = 480 
                win.blit(next_car.get_car, (x, y)) 
                win.blit(kols[i], (x + 43 + x_kol_1, y + 56 + y_kol_1)) 
                win.blit(kols[i], (x + 266 + x_kol_2, y + 56 + y_kol_2)) 
                count += 1

            if -(next_car.width + next_car.speed * 3) + next_car.speed * count == 450:
                first_car_sound.stop() 
                run = False

        pygame.time.delay(50)

        for motion in pygame.event.get():
            if motion.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

    automate = Automate()

    run = True
    click_pay = 0
    while run:
        Screen(next_car.fuel, next_car.count_of_gasoline, next_car.max_gasoline, next_car.count_of_money)
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if button92.makeActive(pos):
                    automate.fuel_type = button92.text
                if button95.makeActive(pos):
                    automate.fuel_type = button95.text
                if button98.makeActive(pos):
                    automate.fuel_type = button98.text
                if buttonExit.makeActive(pos):
                    Exit(text_result, buttonPay, buttonExit)
                    run = False
                inputbox.makeActive(pos)
                card.makeActive(pos)
                if buttonPay.makeActive(pos) and card.active == True:
                    click_pay += Pay(automate, inputbox, text_result, next_car)
                elif buttonPay.makeActive(pos) and card.active == False:
                    text_result.text = "You need to choose a\ncard for use pay button"
            if event.type == pg.KEYDOWN:
                inputbox.inputValue(event)

    run = True
    if click_pay == 0:
        run = False
    count_of_time = time.monotonic()
    count_of_dot = 0
    while run:
        win.blit(bg, (0, 0))

        win.blit(next_car.get_car, (x, y))
        win.blit(kols[i], (x + 43 + x_kol_1, y + 56 + y_kol_1))
        win.blit(kols[i], (x + 266 + x_kol_2, y + 56 + y_kol_2))

        print_text("Refueling", 650, 450, (255, 255, 255), 40)
        if count_of_dot == 0:
            print_text(".", 810, 450, (255, 255, 255), 40)
        elif count_of_dot == 1:
            print_text(".", 810, 450, (255, 255, 255), 40)
            print_text(".", 820, 450, (255, 255, 255), 40)
        elif count_of_dot == 2:
            print_text(".", 810, 450, (255, 255, 255), 40)
            print_text(".", 820, 450, (255, 255, 255), 40)
            print_text(".", 830, 450, (255, 255, 255), 40)
        else:
            print_text(".", 810, 450, (0, 0, 0), 40)
            print_text(".", 820, 450, (0, 0, 0), 40)
            print_text(".", 830, 450, (0, 0, 0), 40)
            count_of_dot = -1
        count_of_dot += 1

        if check_sound_2 == True:
            gasoline_sound.play().set_volume(0.25)
            check_sound_2 = False
        if time.monotonic() - count_of_time >= 11.85:
            run = False
            gasoline_sound.stop()
        for motion in pygame.event.get():
            if motion.type == pygame.QUIT:
                pygame.quit()

        pygame.time.delay(50)
        pygame.display.update()

    run = True
    count_of_time = time.monotonic()
    while run:

        win.blit(bg, (0, 0))

        if time.monotonic() - count_of_time < 4.5:
            win.blit(next_car.get_car, (x, y))
            win.blit(kols[i], (x + 43 + x_kol_1, y + 56 + y_kol_1))
            win.blit(kols[i], (x + 266 + x_kol_2, y + 56 + y_kol_2))
        else:
            i += 1
            if i == 8:
                i = 0
            if -(next_car.width + next_car.speed * 3) + next_car.speed * count < width_win:
                x = -(next_car.width + next_car.speed * 3) + next_car.speed * count
                y = 480
                win.blit(next_car.get_car, (x, y))
                win.blit(kols[i], (x + 43 + x_kol_1, y + 56 + y_kol_1))
                win.blit(kols[i], (x + 266 + x_kol_2, y + 56 + y_kol_2))
                count += 1
        if check_sound_3 == True:
            second_car_sound.play().set_volume(0.25)
            check_sound_3 = False
        if -(next_car.width + next_car.speed * 3) + next_car.speed * count > width_win:
            second_car_sound.stop()
            run = False
            next_button.click_on = False
            next_button.check_on = False
            check_sound_1 = check_sound_2 = check_sound_3 = check_car_position = True
            count = 0
        for motion in pygame.event.get():
            if motion.type == pygame.QUIT:
                pygame.quit()

        pygame.time.delay(50)
        pygame.display.update()

    if check_exit == True:
        pygame.mixer.music.stop()
        return False
    else:
        return True

def Menu():
    run = True
    button_start = Menu_Button(360, 80)
    button_exit = Menu_Button(320, 80)
    while run:
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 1400, 800))

        button_start.draw(width_win - 870, height_win - 700, "START PROGRAM", go)
        button_exit.draw(width_win - 850, height_win - 600, "EXIT PROGRAM", exit)
        print_text("The program was developed by Georgiev Dima and Sekachev German", width_win - 1380, height_win - 100, (255, 255, 255), 25)
        print_text("Group number: 4112", width_win - 1380, height_win - 70, (255, 255, 255), 25)
        print_text("Kazan 2021", width_win - 1380, height_win - 40, (255, 255, 255), 25)
        for motion in pygame.event.get():
            if motion.type == pygame.QUIT:
                run = False

        pygame.time.delay(50)
        pygame.display.update()

Menu()

pygame.quit()