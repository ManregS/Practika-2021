from automate import *

#--------------------Параметры машины--------------------
car_fuel_type = "95"
car_liters = 30
car_liters_MAX = 80
money = 5000
#--------------------------------------------------------

automate = Automate(money=money)

run = True
while run:
    Screen(car_fuel_type, car_liters, car_liters_MAX)
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
            if buttonPay.makeActive(pos):
                Pay(automate, inputbox, text_result, car_fuel_type, car_liters, car_liters_MAX)
            if buttonExit.makeActive(pos):
                run = False
            inputbox.makeActive(pos)
        if event.type == pg.KEYDOWN:
            inputbox.inputValue(event)