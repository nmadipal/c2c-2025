from gpiozero import RGBLED, LED
from matrix_led import MatrixLED, MatrixScanLED
from matrix_led_pin_factory import MatrixLEDPinFactory, MatrixLEDPin, MatrixLEDBoardInfo
from signal import pause
import time
from colorzero import Color

button_count = 16
factory = MatrixLEDPinFactory()
test_rbg = RGBLED('RED1', 'GREEN1', 'BLUE1', pwm=True, pin_factory=factory)
# rgb_leds = []
# led_count = 16
# for idx in range(led_count):
#     rgb_leds.append(RGBLED(f'RED {idx+1}', f'GREEN {idx+1}', f'BLUE {idx+1}', pin_factory=factory))

factory.close()
