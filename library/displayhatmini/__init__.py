#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
import pigpio
from colorsys import hsv_to_rgb

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

    # LCD Backlight Control
    BACKLIGHT = 13

    def __init__(self):
        """Initialise displayhatmini
        """

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


if __name__ == "__main__":
    displayhatmini = DisplayHATMini()

    print("DisplayHATMini Function Test")

    while True:
        if displayhatmini.read_button(displayhatmini.BUTTON_A):
	    displayhatmini.set_led(1.0, 0.0, 0.0)
        elif displayhatmini.read_button(displayhatmini.BUTTON_B):
	    displayhatmini.set_led(1.0, 1.0, 0.0)
        elif displayhatmini.read_button(displayhatmini.BUTTON_X):
	    displayhatmini.set_led(0.0, 1.0, 0.0)
        elif displayhatmini.read_button(displayhatmini.BUTTON_Y):
	    displayhatmini.set_led(0.0, 0.0, 1.0)
        else:
	    displayhatmini.set_led(0.05, 0.05, 0.05)
        time.sleep(0.01)
