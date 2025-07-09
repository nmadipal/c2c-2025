from typing import List

class Button():

    def __init__(self, button_num: int, row_gpio: str, col_gpio: str, red_gpio: str, green_gpio: str, blue_gpio: str, led_col: str,
                 col_idx: int, row_idx: int):
        self.button_num = button_num
        self.col_idx = col_idx
        self.row_idx = row_idx
        self.red_gpio = red_gpio
        self.green_gpio = green_gpio
        self.blue_gpio = blue_gpio
        self.led_col = led_col
        self.row_gpio = row_gpio
        self.col_gpio = col_gpio

    
