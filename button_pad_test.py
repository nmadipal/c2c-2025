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
            # led_list = [red_led, blu_led, grn_led]
            led_col = pad.led_col_list[col]
            if button_state[col][row]:
            #     # If the same button is being pressed, light up the same LED as last time
            #     if last_button_state[col][row] == button_state[col][row]:
            #         led = led_list[last_led_idx[col][row]]
            #     else:
            #         led_idx = random.randint(0, 2)
            #         led = led_list[led_idx]
            #         last_led_idx[col][row] = led_idx                    
                pad.set_led(led, led_col, True)
            else:
                # led = led_list[last_led_idx[col][row]]
                pad.set_led(led, led_col, False)

                
                
                
