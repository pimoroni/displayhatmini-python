#!/usr/bin/env python3
import time
from displayhatmini import DisplayHATMini

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("""This example requires PIL/Pillow, try:

sudo apt install python3-pil

""")

width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT
buffer = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(buffer)
font = ImageFont.load_default()

displayhatmini = DisplayHATMini(buffer, backlight_pwm=True)
displayhatmini.set_led(0.05, 0.05, 0.05)

brightness = 1.0


# Plumbing to convert Display HAT Mini button presses into pygame events
def button_callback(pin):
    global brightness

    # Only handle presses
    if not displayhatmini.read_button(pin):
        return

    if pin == displayhatmini.BUTTON_A:
        brightness += 0.1
        brightness = min(1, brightness)

    if pin == displayhatmini.BUTTON_B:
        brightness -= 0.1
        brightness = max(0, brightness)


displayhatmini.on_button_pressed(button_callback)

draw.rectangle((0, 0, width, height), (255, 255, 255))
draw.text((10, 70), "Backlight Up", font=font, fill=(0, 0, 0))
draw.text((10, 160), "Backlight Down", font=font, fill=(0, 0, 0))

while True:
    displayhatmini.display()
    displayhatmini.set_backlight(brightness)
    time.sleep(1.0 / 30)
