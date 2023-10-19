import time
from PIL import Image, ImageDraw
from . import DisplayHATMini


print("""DisplayHATMini Function Test

Press Ctrl + C to exit!

""")

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
        draw.rectangle((0, height - 50, 50, height), (192, 192, 255))
    else:
        draw.rectangle((0, height - 50, 50, height), (0, 0, 255))

    if displayhatmini.read_button(displayhatmini.BUTTON_X):
        displayhatmini.set_led(0.0, 1.0, 0.0)
        draw.rectangle((width - 50, 0, width, 50), (192, 255, 192))
    else:
        draw.rectangle((width - 50, 0, width, 50), (0, 255, 0))

    if displayhatmini.read_button(displayhatmini.BUTTON_Y):
        displayhatmini.set_led(1.0, 1.0, 0.0)
        draw.rectangle((width - 50, height - 50, width, height), (255, 255, 192))
    else:
        draw.rectangle((width - 50, height - 50, width, height), (255, 255, 0))

    displayhatmini.display()
    time.sleep(0.01)
