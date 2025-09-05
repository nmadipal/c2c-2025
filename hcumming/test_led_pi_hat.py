from gpiozero import RGBLED, LED, ButtonBoard, Button
from matrix_led import MatrixLED, MatrixRGB
from matrix_scan import MatrixScan, MatrixScanButton
from matrix_led_pin_factory import MatrixLEDPinFactory, MatrixLEDPin, MatrixLEDBoardInfo
from matrix_scan_pin_factory import MatrixScanPinFactory, MatrixScanPin, MatrixScanBoardInfo
import time
from colorzero import Color, NAMED_COLORS


button_count = 16
# Create the button and LED factories
button_factory = MatrixScanPinFactory()
led_factory = MatrixLEDPinFactory()
# Create the button board
matrix_button_board = ButtonBoard(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, pull_up=None, active_state=True, pin_factory=button_factory)
# Create the RGB array
rgb_leds = []
for idx in range(button_count):
    rgb_leds.append(RGBLED(f'RED {idx+1}', f'GREEN {idx+1}', f'BLUE {idx+1}', pin_factory=led_factory))

red_led_1 = led_factory.matrix_led.red_leds[0]
red_led_2 = led_factory.matrix_led.red_leds[1]
red_led_3 = led_factory.matrix_led.red_leds[2]
red_led_4 = led_factory.matrix_led.red_leds[3]

green_led_1 = led_factory.matrix_led.green_leds[0]
green_led_2 = led_factory.matrix_led.green_leds[1]
green_led_3 = led_factory.matrix_led.green_leds[2]
green_led_4 = led_factory.matrix_led.green_leds[3]

blue_led_1 = led_factory.matrix_led.blue_leds[0]
blue_led_2 = led_factory.matrix_led.blue_leds[1]
blue_led_3 = led_factory.matrix_led.blue_leds[2]
blue_led_4 = led_factory.matrix_led.blue_leds[3]

led_col_1 = led_factory.matrix_led.led_cols[0]
led_col_2 = led_factory.matrix_led.led_cols[1]
led_col_3 = led_factory.matrix_led.led_cols[2]
led_col_4 = led_factory.matrix_led.led_cols[3]
    
# Update the button scan parameters
scan_delay = 0.004 # 250 Hz
button_factory.matrix_scan.update_scan_delay(scan_delay)
    
# Update the RGB scan parameters
pwm_freq = 10000
display_pause = 0.0004
led_factory.matrix_led.set_pwm_freq(pwm_freq)
led_factory.matrix_led.update_display_pause(display_pause)

# Turn off all LEDs
for rgb_led in rgb_leds:
    rgb_led.color = Color('black')

test_color_list = NAMED_COLORS.keys()

for color in test_color_list:
    color_val = Color(color)
    r_val = color_val.rgb_bytes[0]
    g_val = color_val.rgb_bytes[1]
    b_val = color_val.rgb_bytes[2]
    for rgb_led in rgb_leds:
        rgb_led.color = Color(color)
        print(f'{color}\t-\t{rgb_led_name}: \x1B[48;2;{r_val};{g_val};{b_val}m{tab_seq}       \x1B[40m')
        time.sleep(1)
        for rgb_led in rgb_leds:
            rgb_led.color = Color('black')
        
button_factory.close()
matrix_button_board.close()
led_factory.close()
