import RPi.GPIO as GPIO

class ClGpio():

    def __init__(self, gpio_num: int, direction: str):
        self.gpio_num = gpio_num
        self.direction = direction
        GPIO.setmode(GPIO.BOARD)
        if direction == "in":
            GPIO.setup(gpio_num, GPIO.IN)
        elif direction == "out":
            GPIO.setup(gpio_num, GPIO.OUT)
            # Initialize output to LOW
            GPIO.output(gpio_num, GPIO.LOW)
        else:
            raise ValueError("Direction must be 'in' or 'out'")
        
    def read(self) -> int:
        if self.direction != "in":
            raise RuntimeError("Cannot read from an output GPIO")
        return GPIO.input(self.gpio_num)
    
    def set_level(self, level: int):
        if self.direction != "out":
            raise RuntimeError("Cannot write to an input GPIO")
        GPIO.output(self.gpio_num, level)
