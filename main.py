from automate import *

# Параметры машины
car_fuel_type = "95"
car_liters = 30
car_liters_MAX = 80
money = 5000

# Пользовательский ввод
fuel_type = ""
liters = 0.0

# Основная часть
run = True
while run:
    Screen()
    automate = Automate(fuel_type, liters, money)
    for event in pg.event.get():
        pos = pg.mouse.get_pos()
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if button92.makeActive(pos):
                fuel_type = button92.text
            if button95.makeActive(pos):
                fuel_type = button95.text
            if button98.makeActive(pos):
                fuel_type = button98.text
            if buttonPay.makeActive(pos):
                if inputbox.text != "":
                    automate.liters = float(inputbox.text)
                result = automate.check(car_fuel_type, car_liters, car_liters_MAX)
                text1.printValue(result)
                inputbox.Clear()
                automate.Clear()
            if buttonExit.makeActive(pos):
                run = False
            inputbox.makeActive(pos)
        if event.type == pg.KEYDOWN:
            inputbox.inputValue(event)