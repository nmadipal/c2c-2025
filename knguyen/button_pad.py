
from typing import List
from button import Button

class ButtonPad():

    buttons: List[List[Button]] = [[None for _ in range(4)] for _ in range(4)]

    def __init__(self):
        # Initialize a 4x4 grid of buttons
        button1 = Button(button_num=1, row_gpio_num=40, col_gpio_num=26, red_gpio_num=38, green_gpio_num=37, blue_gpio_num=35, led_col=24)
        # Add rest of button instantiations here

        self.buttons[0][0] = button1
        # Add rest of button assignments here

        # Button number mapping:
        # 1  2  3  4
        # 5  6  7  8
        # 9 10 11 12
        self.button_mapping = [(0,0), (0,1), (0,2), (0,3),
                               (1,0), (1,1), (1,2), (1,3), 
                               (2,0), (2,1), (2,2), (2,3), 
                               (3,0), (3,1), (3,2), (3,3)]
        
    def read_buttons(self) -> List[List[bool]]:
        for button in self.buttons:
            for btn in button:
                btn.read()
        return [[btn.read() for btn in row] for row in self.buttons]

    def read_button(self, button_num: int) -> bool:
        return self.button[self.button_mapping[button_num - 1][0]][self.button_mapping[button_num - 1][1]].read()


if __name__ == "__main__":
    pad = ButtonPad()
    print(pad.read_buttons())
    print(pad.read_button(1))
