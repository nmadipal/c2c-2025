import RPi.GPIO as GPIO

class button_pad:

    def __init__(self):
        # Define the buttons
        self.swt1 = 40
        self.swt2 = 33
        self.swt3 = 21
        self.swt4 = 11

        self.red1 = 38
        self.red2 = 31
        self.red3 = 19
        self.red4 = 7

        self.blu1 = 37
        self.blu2 = 29
        self.blu3 = 15
        self.blu4 = 5

        self.grn1 = 35
        self.grn2 = 23
        self.grn3 = 13
        self.grn4 = 3

        self.led_col1 = 24
        self.led_col2 = 18
        self.led_col3 = 12
        self.led_col4 = 8

        self.swt_col1 = 26
        self.swt_col2 = 22
        self.swt_col3 = 16
        self.swt_col4 = 10

        self.swt_list = [self.swt1, self.swt2, self.swt3, self.swt4]
        self.red_list = [self.red1, self.red2, self.red3, self.red4]
        self.blu_list = [self.blu1, self.blu2, self.blu3, self.blu4]
        self.grn_list = [self.grn1, self.grn2, self.grn3, self.grn4]
        self.led_col_list = \
            [self.led_col1,
             self.led_col2,
             self.led_col3,
             self.led_col4]
        self.swt_col_list = \
            [self.swt_col1,
             self.swt_col2,
             self.swt_col3,
             self.swt_col4]

        self.led_dict = {}
        self.swt_dict = {}
        self.led_col_dict = {}
        self.swt_col_dict = {}
    
        self.max_debounce = 3
        
        GPIO.setmode(GPIO.BOARD)

        for idx in range(len(self.led_col_list)):
            red_led = self.red_list[idx]
            blu_led = self.blu_list[idx]
            grn_led = self.grn_list[idx]
            led_col = self.led_col_list[idx]
            self.led_dict[red_led] = led_col
            self.led_dict[blu_led] = led_col
            self.led_dict[grn_led] = led_col
            self.led_col_dict[led_col] = [red_led, blu_led, grn_led]

        for idx in range(len(self.swt_col_list)):
            swt = self.swt_list[idx]
            swt_col = self.swt_col_list[idx]
            self.swt_dict[swt] = swt_col
            self.swt_col_dict[swt_col] = [swt]
            
        self.initialize_board()
        
    def initialize_board(self):
        for swt in self.swt_list:
            GPIO.setup(swt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        for red in self.red_list:
            GPIO.setup(red, GPIO.OUT)
            GPIO.output(red, GPIO.LOW)

        for blu in self.blu_list:
            GPIO.setup(blu, GPIO.OUT)
            GPIO.output(blu, GPIO.LOW)

        for grn in self.grn_list:
            GPIO.setup(grn, GPIO.OUT)
            GPIO.output(grn, GPIO.LOW)

        for led_col in self.led_col_list:
            GPIO.setup(led_col, GPIO.OUT)
            GPIO.output(led_col, GPIO.HIGH)

        for swt_col in self.swt_col_list:
            GPIO.setup(swt_col, GPIO.OUT)
            GPIO.output(swt_col, GPIO.HIGH)

    def poll_led_col(self, led_col):
        # Return list of states of LEDs in a column
        led_list = self.led_col_dict[led_col]
        led_state_list = []
        for led in led_list:
            led_state_list.append(GPIO.input(led))
        return led_state_list
            
    def set_led(self, led, led_col, enable_led):
        if enable_led:
            # print(f'DEBUG: led: {led} led_col: {led_col}')
            GPIO.output(led, GPIO.HIGH)
            GPIO.output(led_col, GPIO.LOW)
            # If the LED column is not enabled, then enable the column
            # if GPIO.input(led_col):
            #    GPIO.output (led_col, GPIO.LOW)
        else:
            GPIO.output(led, GPIO.LOW)
            GPIO.output(led_col, GPIO.HIGH)
            # led_state_list = self.poll_led_col(led_col)
            # If all the LEDs in a column are off, turn off the column as well
            # if all([val == 0 for val in led_state_list]):
            #     GPIO.output(led_col, GPIO.HIGH)

    def poll_switches(self):
        button_state = [[0 for col in range(len(self.swt_col_list))] for row in range(len(self.swt_list))]
        col_idx = 0
        for swt_col in self.swt_col_list:
            GPIO.output(swt_col, GPIO.LOW)
            row_idx = 0
            for swt in self.swt_list:
                # print(f'DEBUG: COL = {swt_col} ROW = {swt}')
                debounce_val_list = []
                for count in range(self.max_debounce):
                    debounce_val_list.append(GPIO.input(swt))
                if all([val == 0 for val in debounce_val_list]):
                    button_state[col_idx][row_idx] = 1
                else:
                    button_state[col_idx][row_idx] = 0
                row_idx += 1
            GPIO.output(swt_col, GPIO.HIGH)
            col_idx += 1
        return button_state


            
