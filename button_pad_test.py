from button_pad import button_pad
import random

pad = button_pad()
col_count = 4
row_count = 4

last_button_state = pad.poll_switches()
last_led_idx = [[0 for col in range(col_count)] for row in range(row_count)]

while(True):
    button_state = pad.poll_switches()
    for col in range(col_count):
        for row in range(row_count):
            red_led = pad.red_list[row]
            blu_led = pad.blu_list[row]
            grn_led = pad.grn_list[row]
            led = blu_led
            led_col = pad.led_col_list[col]
            if button_state[col][row]:            
                pad.set_led(led, led_col, True)
            else:
                pad.set_led(led, led_col, False)

                
                
                
