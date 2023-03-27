#!/usr/bin/env python3
import time

from displayhatmini import DisplayHATMini


class LED:
    def __init__(self):
        self.displayhatmini = DisplayHATMini(buffer=None, backlight_pwm=True)
        self.displayhatmini.on_button_pressed(self.button_callback)
        self.r = 0
        self.g = 0
        self.b = 0
        self.update()

    def __del__(self):
        # Turn off the LED (this gets called even if we are interrupted)
        self.displayhatmini.set_led(0, 0, 0)

    def button_callback(self, pin):
        # Only handle presses
        if not self.displayhatmini.read_button(pin):
            return

        if pin == DisplayHATMini.BUTTON_A:
            self.r = 1 - self.r
        elif pin == DisplayHATMini.BUTTON_B:
            self.g = 1 - self.g
        elif pin == DisplayHATMini.BUTTON_X:
            self.b = 1 - self.b

        self.update()

    def update(self):
        self.displayhatmini.set_led(
            self.r * 0.05, self.g * 0.05, self.b * 0.05
        )


led = LED()
while True:
    time.sleep(1.0 / 30)
