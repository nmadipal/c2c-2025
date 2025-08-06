from gpiozero import RGBLED, LED, ButtonBoard, Button
from matrix_led import MatrixLED, MatrixRGB
from matrix_scan import MatrixScan, MatrixScanButton
from matrix_led_pin_factory import MatrixLEDPinFactory, MatrixLEDPin, MatrixLEDBoardInfo
from matrix_scan_pin_factory import MatrixScanPinFactory, MatrixScanPin, MatrixScanBoardInfo
import time
from colorzero import Color

class MatrixButtonLEDController:
    def __init__(self, button_count = 16, scan_delay=0.004, pwm_freq=10000, display_pause=0.0004):
        self.button_count = button_count
        self.scan_delay = scan_delay
        self.pwm_freq = pwm_freq
        self.display_pause = display_pause

        # Initialize factories
        self.button_factory = MatrixScanPinFactory()
        self.led_factory = MatrixLEDPinFactory()

        # Create the button board
        self.matrix_button_board = ButtonBoard(
            *range(1, button_count + 1),
            pull_up=None,
            active_state=True,
            pin_factory=self.button_factory
        )

        # Create the RGB LED array
        self.rgb_leds = [
            RGBLED(f'RED {idx+1}', f'GREEN {idx+1}', f'BLUE {idx+1}', pin_factory=self.led_factory)
            for idx in range(button_count)
        ]

        # Configure scan parameters
        self._configure_scan_parameters()

        # Assign button events
        self._assign_button_events()

    def _configure_scan_parameters(self):
        # Update button scan parameters
        self.button_factory.matrix_scan.update_scan_delay(self.scan_delay)

        # Update RGB scan parameters
        self.led_factory.matrix_led.set_pwm_freq(self.pwm_freq)
        self.led_factory.matrix_led.update_display_pause(self.display_pause)

    def _assign_button_events(self):
        for button in range(self.button_count):
            self.matrix_button_board[button].when_pressed = self.light_when_pressed
            self.matrix_button_board[button].when_held = self.light_when_held
            self.matrix_button_board[button].when_released = self.light_when_released

    def light_when_pressed(self, button):
        button_idx = button.pin.info.number
        self.rgb_leds[button_idx - 1].color = Color('green')

    def light_when_held(self, button):
        button_idx = button.pin.info.number
        self.rgb_leds[button_idx - 1].color = Color('red')

    def light_when_released(self, button):
        button_idx = button.pin.info.number
        self.rgb_leds[button_idx - 1].color = Color('blue')

    def run(self):
        try:
            input('Press <ENTER> to close the test')
        finally:
            self.cleanup()

    def cleanup(self):
        self.button_factory.close()
        self.matrix_button_board.close()


# Example usage
if __name__ == "__main__":
    button_count = 16  # Adjust as needed
    controller = MatrixButtonLEDController(button_count)
    controller.run()