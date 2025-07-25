from gpiozero import RGBLED, LED, ButtonBoard, Button
from matrix_led import MatrixLED, MatrixRGB
from matrix_scan import MatrixScan, MatrixScanButton
from matrix_led_pin_factory import MatrixLEDPinFactory, MatrixLEDPin, MatrixLEDBoardInfo
from matrix_scan_pin_factory import MatrixScanPinFactory, MatrixScanPin, MatrixScanBoardInfo
import time
from colorzero import Color


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

# Update the button scan parameters
scan_delay = 0.004 # 250 Hz
button_factory.matrix_scan.update_scan_delay(scan_delay)
    
# Update the RGB scan parameters
pwm_freq = 10000
display_pause = 0.0004
led_factory.matrix_led.set_pwm_freq(pwm_freq)
led_factory.matrix_led.update_display_pause(display_pause)

# Assign the LEDs

def light_when_pressed(button):
    button_idx = button.pin.info.number
    rgb_leds[button_idx-1].color = Color('green')
    

def light_when_held(button):
    button_idx = button.pin.info.number
    rgb_leds[button_idx-1].color = Color('red')

def light_when_released(button):
    button_idx = button.pin.info.number
    rgb_leds[button_idx-1].color = Color('blue')



for button in range(button_count):
    matrix_button_board[button].when_pressed = light_when_pressed
    matrix_button_board[button].when_held = light_when_held
    matrix_button_board[button].when_released = light_when_released


input('Press <ENTER> to close the test')


button_factory.close()
matrix_button_board.close()
led_factory.close()
    
    
