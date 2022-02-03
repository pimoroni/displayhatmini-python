#!/usr/bin/env python3
import os
import sys
import signal
import pygame
import time
import math
from threading import Lock

from displayhatmini import DisplayHATMini


print("""Display HAT Mini: Basic Pygame Demo""")

if pygame.vernum < (2, 0, 0):
    print("Need PyGame >= 2.0.0:\n    python3 -m pip install pygame --upgrade")
    sys.exit(1)


def _exit(sig, frame):
    global running
    running = False
    print("\nExiting!...\n")


def update_display():
    display_hat.st7789.set_window()
    # Grab the pygame screen as a bytes object
    pixelbytes = pygame.transform.rotate(screen, 180).convert(16, 0).get_buffer()
    # Lazy (slow) byteswap:
    pixelbytes = bytearray(pixelbytes)
    pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
    # Bypass the ST7789 PIL image RGB888->RGB565 conversion
    for i in range(0, len(pixelbytes), 4096):
        display_hat.st7789.data(pixelbytes[i:i + 4096])


display_hat = DisplayHATMini(None)
event_lock = Lock()

os.putenv('SDL_VIDEODRIVER', 'dummy')
pygame.display.init()  # Need to init for .convert() to work
screen = pygame.Surface((display_hat.WIDTH, display_hat.HEIGHT))

signal.signal(signal.SIGINT, _exit)


# Plumbing to convert Display HAT Mini button presses into pygame events
def button_callback(pin):
    key = {
        display_hat.BUTTON_A: 'a',
        display_hat.BUTTON_B: 'b',
        display_hat.BUTTON_X: 'x',
        display_hat.BUTTON_Y: 'y'
    }[pin]
    event = pygame.KEYDOWN if display_hat.read_button(pin) else pygame.KEYUP
    pygame.event.post(pygame.event.Event(event, unicode=key, key=pygame.key.key_code(key)))


display_hat.on_button_pressed(button_callback)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_ESCAPE):
                running = False
                break

    # Clear the screen
    screen.fill((0, 0, 0))

    box_w = display_hat.WIDTH // 3
    box_h = display_hat.HEIGHT // 2

    pygame.draw.rect(screen, (255, 0, 0), (0, 0, box_w, box_h))
    pygame.draw.rect(screen, (0, 255, 0), (box_w, 0, box_w, box_h))
    pygame.draw.rect(screen, (0, 0, 255), (box_w * 2, 0, box_w, box_h))

    pygame.draw.rect(screen, (255, 255, 0), (0, box_h, box_w, box_h))
    pygame.draw.rect(screen, (255, 0, 255), (box_w, box_h, box_w, box_h))
    pygame.draw.rect(screen, (0, 255, 255), (box_w * 2, box_h, box_w, box_h))

    r = 50
    x = math.sin(time.time() * 2) * (display_hat.WIDTH - r) / 2
    y = math.cos(time.time()) * (display_hat.HEIGHT - r) / 2
    x += display_hat.WIDTH // 2
    y += display_hat.HEIGHT // 2
    pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), r)

    update_display()


screen.fill((0, 0, 0))
update_display()

pygame.quit()
sys.exit(0)