#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
from ST7789 import ST7789
from PIL import Image, ImageDraw

__version__ = '0.0.1'

class DisplayHATMini():
    # User buttons
    BUTTON_A = 5
    BUTTON_B = 6
    BUTTON_X = 16
    BUTTON_Y = 24

    # Onboard RGB LED
    LED_R = 17
    LED_G = 27
    LED_B = 22

    # LCD Pins
    SPI_PORT = 0
    SPI_CS = 1
    SPI_DC = 9
    BACKLIGHT = 13

    # LCD Size
    WIDTH = 320
    HEIGHT = 240

    def __init__(self, buffer):
        """Initialise displayhatmini
        """

        self.buffer = buffer
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Setup user buttons
        GPIO.setup(self.BUTTON_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON_X, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON_Y, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Setup user LEDs
        GPIO.setup(self.LED_R, GPIO.OUT)
        GPIO.setup(self.LED_G, GPIO.OUT)
        GPIO.setup(self.LED_B, GPIO.OUT)

        self.led_r_pwm = GPIO.PWM(self.LED_R, 2000)
        self.led_r_pwm.start(100)

        self.led_g_pwm = GPIO.PWM(self.LED_G, 2000)
        self.led_g_pwm.start(100)

        self.led_b_pwm = GPIO.PWM(self.LED_B, 2000)
        self.led_b_pwm.start(100)

        self.st7789 = ST7789(
            port=self.SPI_PORT,
            cs=self.SPI_CS,
            dc=self.SPI_DC,
            backlight=self.BACKLIGHT,
            width=self.WIDTH,
            height=self.HEIGHT,
            rotation=180,
            spi_speed_hz=60 * 1000 * 1000
        )

    def __del__(self):
        GPIO.cleanup()

    def set_led(self, r=0, g=0, b=0):
        if r < 0.0 or r > 1.0:
            raise ValueError("r must be in the range 0.0 to 1.0")
        elif g < 0.0 or g > 1.0:
            raise ValueError("g must be in the range 0.0 to 1.0")
        elif b < 0.0 or b > 1.0:
            raise ValueError("b must be in the range 0.0 to 1.0")
        else:
            self.led_r_pwm.ChangeDutyCycle((1.0 - r) * 100)
            self.led_g_pwm.ChangeDutyCycle((1.0 - g) * 100)
            self.led_b_pwm.ChangeDutyCycle((1.0 - b) * 100)

    def read_button(self, pin):
        return not GPIO.input(pin)

    def display(self):
        self.st7789.display(self.buffer)


if __name__ == "__main__":
    print("DisplayHATMini Function Test")

    width = DisplayHATMini.WIDTH
    height = DisplayHATMini.HEIGHT
    buffer = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(buffer)

    displayhatmini = DisplayHATMini(buffer)
    displayhatmini.set_led(0.05, 0.05, 0.05)

    while True:
        draw.rectangle((0, 0, width, height), (0, 0, 0))

        if displayhatmini.read_button(displayhatmini.BUTTON_A):
            displayhatmini.set_led(1.0, 0.0, 0.0)
            draw.rectangle((0, 0, 50, 50), (255, 192, 192))
        else:
            draw.rectangle((0, 0, 50, 50), (255, 0, 0))

        if displayhatmini.read_button(displayhatmini.BUTTON_B):
            displayhatmini.set_led(0.0, 0.0, 1.0)
            draw.rectangle((0, height-50, 50, height), (192, 192, 255))
        else:
            draw.rectangle((0, height-50, 50, height), (0, 0, 255))

        if displayhatmini.read_button(displayhatmini.BUTTON_X):
            displayhatmini.set_led(0.0, 1.0, 0.0)
            draw.rectangle((width-50, 0, width, 50), (192, 255, 192))
        else:
            draw.rectangle((width-50, 0, width, 50), (0, 255, 0))            

        if displayhatmini.read_button(displayhatmini.BUTTON_Y):
            displayhatmini.set_led(1.0, 1.0, 0.0)
            draw.rectangle((width-50, height-50, width, height), (255, 255, 192))
        else:
            draw.rectangle((width-50, height-50, width, height), (255, 255, 0))

        displayhatmini.display()
        time.sleep(0.01)
