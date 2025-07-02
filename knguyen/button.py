
from typing import List
from led import Led
from cl_gpio import Clgpio

class Button():

    def __init__(self, row_gpio_num: int, col_gpio_num: int, red_gpio_num: int, green_gpio_num: int, blue_gpio_num: int, led_col: int):
        self.led = Led(red_gpio_num, green_gpio_num, blue_gpio_num, led_col)
        self.row_gpio = Clgpio(row_gpio_num, "in")
        self.col_gpio = Clgpio(col_gpio_num, "out")

    def read(self) -> bool:
        # Set col_gpio to LOW 
        # read row_gpio
        # if row_gpio is HIGH, button is pressed
        # else button is not pressed
        return False

    def set_color(self, red: int, green: int, blue: int):
        self.led.set_color(red, green, blue)

    def turn_off(self):
        self.led.turn_off()

    def turn_on(self):
        self.led.turn_on()

    