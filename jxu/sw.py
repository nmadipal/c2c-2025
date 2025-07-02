import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BOARD)

# Define your pin mappings
swt_rows = [40, 33, 21, 11]   # GPIO 21,13,9,17
swt_cols = [26, 22, 16, 10]   # GPIO 7,25,23,15
# Anode rows for red, green, blue
red_pins = [38, 31, 19, 7]
grn_pins = [35, 23, 13, 3]
blu_pins = [37, 29, 15, 5]

# Cathode columns
led_cols = [24, 18, 12, 8]

# Setup all pins
for pin in red_pins + grn_pins + blu_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in led_cols:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def light_led(x, y, r, g, b, duration=0.05):
    if not (0 <= x < 4 and 0 <= y < 4):
        return
    # Clear all
    for i in range(4):
        GPIO.output(red_pins[i], GPIO.LOW)
        GPIO.output(grn_pins[i], GPIO.LOW)
        GPIO.output(blu_pins[i], GPIO.LOW)
        GPIO.output(led_cols[i], GPIO.HIGH)
    # Set colors
    if r: GPIO.output(red_pins[x], GPIO.HIGH)
    if g: GPIO.output(grn_pins[x], GPIO.HIGH)
    if b: GPIO.output(blu_pins[x], GPIO.HIGH)
    # Enable column
    GPIO.output(led_cols[y], GPIO.LOW)
    time.sleep(duration)
    # Turn off
    GPIO.output(red_pins[x], GPIO.LOW)
    GPIO.output(grn_pins[x], GPIO.LOW)
    GPIO.output(blu_pins[x], GPIO.LOW)
    GPIO.output(led_cols[y], GPIO.HIGH)
# === Faster scan using monotonic_ns ===
def display_rgb_matrix(matrix, duration=1.0, row_time_us=500):
    """
    Display a 4x4 RGB matrix using precise microsecond row timing.

    matrix: 4x4 list of [r,g,b] values (0 or 1)
    duration: total time to display matrix (in seconds)
    row_time_us: how long to scan each row (in microseconds)
    """

    end_time_ns = time.monotonic_ns() + int(duration * 1e9)
    row_time_ns = int(row_time_us * 1000)

    while time.monotonic_ns() < end_time_ns:
        for row in range(4):
            start_ns = time.monotonic_ns()

            # Turn off all columns and colors
            for col_pin in led_cols:
                GPIO.output(col_pin, GPIO.HIGH)
            for pin in red_pins + grn_pins + blu_pins:
                GPIO.output(pin, GPIO.LOW)

            # Set RGB for this row
            for col in range(4):
                r, g, b = matrix[row][col]
                if r: GPIO.output(red_pins[row], GPIO.HIGH)
                if g: GPIO.output(grn_pins[row], GPIO.HIGH)
                if b: GPIO.output(blu_pins[row], GPIO.HIGH)
                GPIO.output(led_cols[col], GPIO.LOW)

            # Wait precisely for the row time
            # while time.monotonic_ns() - start_ns < row_time_ns:
            #     pass  # tight loop instead of sleep

            # Turn off row before next
            for col in range(4):
                GPIO.output(led_cols[col], GPIO.HIGH)
            GPIO.output(red_pins[row], GPIO.LOW)
            GPIO.output(grn_pins[row], GPIO.LOW)
            GPIO.output(blu_pins[row], GPIO.LOW)

def setup_pins():
    GPIO.setmode(GPIO.BOARD)  # or GPIO.BCM if using BCM numbers
    for row in swt_rows:
        GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for col in swt_cols:
        GPIO.setup(col, GPIO.OUT)
        GPIO.output(col, GPIO.HIGH)

def read_keypad():
    keys = [[0 for _ in range(4)] for _ in range(4)]

    for col_index, col_pin in enumerate(swt_cols):
        # Activate one column
        GPIO.output(col_pin, GPIO.LOW)
        time.sleep(0.001)  # settle time

        for row_index, row_pin in enumerate(swt_rows):
            if GPIO.input(row_pin) == GPIO.LOW:
                keys[row_index][col_index] = 1  # Key pressed

        GPIO.output(col_pin, GPIO.HIGH)  # Deactivate column

    return keys
display_matrix = [
        [[0,0,0], [0,0,0], [0,0,0], [0,0,0]],
        [[0,0,0], [0,0,0], [0,0,0], [0,0,0]],
        [[0,0,0], [0,0,0], [0,0,0], [0,0,0]],
        [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
            ]
# Example usage
if __name__ == "__main__":
    try:
        setup_pins()
        while True:
            matrix = read_keypad()
 
            #print(matrix)
            r = random.randint(0, 1)
            g = random.randint(0, 1)
            b = random.randint(0, 1)
            for col_index, col_value in enumerate(matrix):
                for row_index, row_value in enumerate(col_value):
                    if row_value ==1:
                        light_led(col_index, row_index, r, g, b, duration=0.01)

    except KeyboardInterrupt:
        GPIO.cleanup()
