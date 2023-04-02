import subprocess
import time
from datetime import datetime, timezone
from threading import Timer

from displayhatmini import DisplayHATMini
from netifaces import interfaces, ifaddresses, AF_INET
from PIL import Image, ImageDraw, ImageFont

width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT
buffer = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(buffer)
font = ImageFont.load_default()

displayhatmini = DisplayHATMini(buffer, backlight_pwm=True)
displayhatmini.set_led(0.1, 0, 0)


def display_ip():
    print("Working out ip addresses...")
    ip_str_lines = []
    for ifaceName in interfaces():
        addresses = [
            i["addr"]
            for i in ifaddresses(ifaceName).setdefault(
                AF_INET, [{"addr": "No IP addr"}]
            )
        ]
        ip_str_lines.append(f"{ifaceName}: {' '.join(addresses)}")

    print("\n".join(ip_str_lines))

    y = 20
    for line in ip_str_lines:
        draw.text(
            xy=(10, y), text=line, fill=(255, 255, 255), font=font
        )
        y += 20


def display_time():
    timestr = datetime.now(tz=timezone.utc).astimezone().strftime("%H:%M:%S")
    draw.rectangle(
        xy=(0, height // 2 - 20, width, height // 2 + 10),
        fill=(0, 0, 0),
    )
    draw.text(
        xy=((width - font.getlength(timestr)) // 2, height // 2),
        text=timestr,
        fill=(255, 255, 255),
        font=font,
    )
    Timer(0.5, display_time).start()


def display_uptime():
    uptime = subprocess.run(
        "uptime", stdout=subprocess.PIPE
    ).stdout.decode("utf-8").strip()

    idx = uptime.index("load")

    draw.rectangle(xy=(0, height-30, (width * 2) // 3, height), fill=(0, 0, 0))
    draw.text(xy=(0, height-30), text=uptime[:idx], fill=(255, 255, 255), font=font)
    draw.text(xy=(0, height-15), text=uptime[idx:], fill=(255, 255, 255), font=font)
    Timer(15, display_uptime).start()


def button_callback(pin):
    if not displayhatmini.read_button(pin):
        return

    display_ip()


displayhatmini.on_button_pressed(button_callback)
displayhatmini.set_backlight(1.0)
display_ip()
display_time()
display_uptime()

while True:
    displayhatmini.display()
    time.sleep(1.0 / 30)
