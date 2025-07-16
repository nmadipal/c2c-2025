from gpiozero import RGBLED, LEDBoard
from colorzero import Color
from typing import List
from time import sleep
from gpiozero.threads import GPIOThread


class MatrixLED(GPIOThread):

    def __init__(self, pwm_freq = 0, display_pause=0.01):
        super().__init__(target=self._run_led_matrix)
        self.daemon = True

        self.red1 = 'BOARD38'
        self.red2 = 'BOARD31'
        self.red3 = 'BOARD19'
        self.red4 = 'BOARD7'

        self.blue1 = 'BOARD35'
        self.blue2 = 'BOARD23'
        self.blue3 = 'BOARD13'
        self.blue4 = 'BOARD3'

        self.green1 = 'BOARD37'
        self.green2 = 'BOARD29'
        self.green3 = 'BOARD15'
        self.green4 = 'BOARD5'
        
        self.led_col1 = 'BOARD24'
        self.led_col2 = 'BOARD18'
        self.led_col3 = 'BOARD12'
        self.led_col4 = 'BOARD8'

        if pwm_freq is None or pwm_freq == 0:
            self.pwm = False
        else:
            self.pwm = True
        self.red_leds = LEDBoard(self.red4, self.red3, self.red2, self.red1, active_high=True, pwm=self.pwm)
        self.blue_leds = LEDBoard(self.blue4, self.blue3, self.blue2, self.blue1, active_high = True, pwm=self.pwm)
        self.green_leds = LEDBoard(self.green4, self.green3, self.green2, self.green1, active_high = True, pwm=self.pwm)
        self.led_cols = LEDBoard(self.led_col1, self.led_col2, self.led_col3, self.led_col4, active_high= False, pwm=False)

        self.enable_leds = False
        self.display_pause = display_pause

        self.red_led_map = {
            1: MatrixScanLED(row=0, col=0),
            2: MatrixScanLED(row=0, col=1),
            3: MatrixScanLED(row=0, col=2),
            4: MatrixScanLED(row=0, col=3),
            5: MatrixScanLED(row=1, col=0),
            6: MatrixScanLED(row=1, col=1),
            7: MatrixScanLED(row=1, col=2),
            8: MatrixScanLED(row=1, col=3),
            9: MatrixScanLED(row=2, col=0),
            10: MatrixScanLED(row=2, col=1),
            11: MatrixScanLED(row=2, col=2),
            12: MatrixScanLED(row=2, col=3),
            13: MatrixScanLED(row=3, col=0),
            14: MatrixScanLED(row=3, col=1),
            15: MatrixScanLED(row=3, col=2),
            16: MatrixScanLED(row=3, col=3)
            }

        self.blue_led_map = {
            1: MatrixScanLED(row=0, col=0),
            2: MatrixScanLED(row=0, col=1),
            3: MatrixScanLED(row=0, col=2),
            4: MatrixScanLED(row=0, col=3),
            5: MatrixScanLED(row=1, col=0),
            6: MatrixScanLED(row=1, col=1),
            7: MatrixScanLED(row=1, col=2),
            8: MatrixScanLED(row=1, col=3),
            9: MatrixScanLED(row=2, col=0),
            10: MatrixScanLED(row=2, col=1),
            11: MatrixScanLED(row=2, col=2),
            12: MatrixScanLED(row=2, col=3),
            13: MatrixScanLED(row=3, col=0),
            14: MatrixScanLED(row=3, col=1),
            15: MatrixScanLED(row=3, col=2),
            16: MatrixScanLED(row=3, col=3)
            }

        self.green_led_map = {
            1: MatrixScanLED(row=0, col=0),
            2: MatrixScanLED(row=0, col=1),
            3: MatrixScanLED(row=0, col=2),
            4: MatrixScanLED(row=0, col=3),
            5: MatrixScanLED(row=1, col=0),
            6: MatrixScanLED(row=1, col=1),
            7: MatrixScanLED(row=1, col=2),
            8: MatrixScanLED(row=1, col=3),
            9: MatrixScanLED(row=2, col=0),
            10: MatrixScanLED(row=2, col=1),
            11: MatrixScanLED(row=2, col=2),
            12: MatrixScanLED(row=2, col=3),
            13: MatrixScanLED(row=3, col=0),
            14: MatrixScanLED(row=3, col=1),
            15: MatrixScanLED(row=3, col=2),
            16: MatrixScanLED(row=3, col=3)
            }

        self.led_pos_map = {
            1: (0, 0),
            2: (0, 1),
            3: (0, 2),
            4: (0, 3),
            5: (1, 0),
            6: (1, 1),
            7: (1, 2),
            8: (1, 3),
            9: (2, 0),
            10: (2, 1),
            11: (2, 2),
            12: (2, 3),
            13: (3, 0),
            14: (3, 1),
            15: (3, 2),
            16: (3, 3)
            }

        self.pos_led_map = dict((v,k) for k,v in self.led_pos_map.items())

        self.disable_led_columns()
        self.disable_red_leds()
        self.disable_blue_leds()
        self.disable_green_leds()
        self.set_pwm_freq(pwm_freq)

    def disable_led_columns(self):
        self.led_cols.off()

    def disable_red_leds(self):
        self.red_leds.off()
        for led_num in self.red_led_map.keys():
            self.red_led_map[led_num].next_state = 0

    def disable_blue_leds(self):
        self.blue_leds.off()
        for led_num in self.blue_led_map.keys():
            self.blue_led_map[led_num].next_state = 0

    def disable_green_leds(self):
        self.green_leds.off()
        for led_num in self.green_led_map.keys():
            self.green_led_map[led_num].next_state = 0
        
    def lookup_led_number(self, row, col):
        return self.pos_led_map[(row,col)]

    def lookup_led_pos(self, led_number):
        return self.led_pos_map[led_number]

    def stop_led_matrix(self):
        self.enable_leds = False
        sleep(0.1)
        self.disable_led_columns()
        self.disable_red_leds()
        self.disable_blue_leds()
        self.disable_green_leds()

    def start_led_matrix(self):
        self.enable_leds = True

    def _run_led_matrix(self):
        while self.enable_leds and not self.stopping.is_set():
            self.disp_led_matrix()

    def _update_leds(self, led_number):
        led_row, led_col = self.lookup_led_pos(led_number)
        red_led = self.red_leds[led_row]
        blue_led = self.blue_leds[led_row]
        green_led = self.green_leds[led_row]
        ticks = red_led.pin.factory.ticks()
        if self.red_led_map[led_number].next_state != self.red_led_map[led_number].state:
            self.red_led_map[led_number].change_ticks = ticks
        if self.blue_led_map[led_number].next_state != self.blue_led_map[led_number].state:
            self.blue_led_map[led_number].change_ticks = ticks
        if self.green_led_map[led_number].next_state != self.green_led_map[led_number].state:
            self.green_led_map[led_number].change_ticks = ticks
        self.red_led_map[led_number].state = self.red_led_map[led_number].next_state
        self.blue_led_map[led_number].state = self.blue_led_map[led_number].next_state
        self.green_led_map[led_number].state = self.green_led_map[led_number].next_state
        if self.red_led_map[led_number].state:
            red_led.on()
        else:
            red_led.off()
        if self.blue_led_map[led_number].state:
            blue_led.on()
        else:
            blue_led.off()
        if self.green_led_map[led_number].state:
            green_led.on()
        else:
            green_led.off()

    def _turn_off_row(self, row_idx):
        self.red_leds[row_idx].off()
        self.blue_leds[row_idx].off()
        self.green_leds[row_idx].off()
                     
    def disp_led_matrix(self):
        if self.enable_leds and not self.stopping.is_set():
            for col_idx, col in enumerate(self.led_cols):
                for row_idx, _ in enumerate(self.red_leds):
                    led_num = self.lookup_led_number(row_idx, col_idx)
                    # Update the LED colors
                    self._update_leds(led_num)
                # Strobe the LED column
                col.on()
                sleep(self.display_pause)
                col.off()
                # Turn off the LEDs
                for row_idx, _ in enumerate(self.red_leds):
                    self._turn_off_row(row_idx)

    def disable_led(self, led_color, led_num):
        self.set_led_state(led_color, led_num, 0)
        
    def enable_led(self, led_color, led_num):
        self.set_led_state(led_color, led_num, 1)
        
    def release_led_matrix(self):
        self.stop_led_matrix()
        self.red_leds.close()
        self.blue_leds.close()
        self.green_leds.close()
        self.led_cols.close()
        self.stop()

    def get_led_state(self, led_color, led_num):
        if led_color == 'red':
            return self.red_led_map[led_num].state
        elif led_color == 'blue':
            return self.blue_led_map[led_num].state
        elif led_color == 'green':
            return self.green_led_map[led_num].state

    def set_led_state(self, led_color, led_num, state):
        if led_color == 'red':
            self.red_led_map[led_num].next_state = state
        elif led_color == 'blue':
            self.blue_led_map[led_num].next_state = state
        elif led_color == 'green':
            self.green_led_map[led_num].next_state = state
    
    def update_display_pause(self, display_pause):
        self.display_pause = display_pause

    def set_pwm_freq(self, value):
        if self.pwm:
            for led in self.red_leds:
                led.frequency = value
            for led in self.blue_leds:
                led.frequency = value
            for led in self.green_leds:
                led.frequency = value
            self.pwm_freq = value

    def get_pwm_freq(self):
        return self.pwm_freq    

class MatrixScanLED:

    # row: row of LED on pad
    # col: column of LED on pad
    # next_state: Next state the LED will be set to
    # state: State of the LED
    # change_ticks: Time when the state changed
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.next_state = 0
        self.state = 0
        self.change_ticks = None

    


