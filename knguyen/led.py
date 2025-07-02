
from typing import List
from cl_gpio import Clgpio

class Led():

    def __init__(self, red_gpio_num: int, green_gpio_num: int, blue_gpio_num: int, cathode_gpio_num: int):
        self.red_gpio = Clgpio(red_gpio_num, "out")
        self.green_gpio = Clgpio(green_gpio_num, "out")
        self.blue_gpio = Clgpio(blue_gpio_num, "out")
        self.cathode_gpio = Clgpio(cathode_gpio_num, "out")
        
    def set_color(self, red: int, green: int, blue: int):
        self.red_gpio.set_level(red)
        self.green_gpio.set_level(green)
        self.blue_gpio.set_level(blue)  

    def turn_off(self):
        self.cathode_gpio.set_level(1)  # Assuming active low for cathode

    def turn_on(self): 
        self.cathode_gpio.set_level(0)  # Assuming active low for cathode

    