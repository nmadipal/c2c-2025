import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

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
            while time.monotonic_ns() - start_ns < row_time_ns:
                pass  # tight loop instead of sleep

            # Turn off row before next
            for col in range(4):
                GPIO.output(led_cols[col], GPIO.HIGH)
            GPIO.output(red_pins[row], GPIO.LOW)
            GPIO.output(grn_pins[row], GPIO.LOW)
            GPIO.output(blu_pins[row], GPIO.LOW)

try:
    matrix = [
        [[1,0,0], [0,1,0], [0,0,1], [1,1,0]],
        [[0,1,1], [1,0,1], [1,1,1], [0,0,0]],
        [[1,0,0], [1,0,0], [0,1,0], [0,0,1]],
        [[1,1,1], [0,0,0], [1,1,0], [0,1,1]]
    ]
    while True:
        display_rgb_matrix(matrix, duration=0.5, row_time_us=500)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
