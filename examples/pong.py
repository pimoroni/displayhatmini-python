#!/usr/bin/env python3
import random
import time
import math
from displayhatmini import DisplayHATMini
from collections import namedtuple
from turtle import Vec2D

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

displayhatmini = DisplayHATMini(buffer)
displayhatmini.set_led(0.05, 0.05, 0.05)


Position = namedtuple('Position', 'x y')
Size = namedtuple('Size', 'w h')


def millis():
    return int(round(time.time() * 1000))


def text(draw, text, position, size, color):
    fnt = ImageFont.load_default()
    draw.text(position, text, font=fnt, fill=color)


class Ball():
    def __init__(self):
        global width, height
        self.position = Vec2D(width / 2, height / 2)
        self.velocity = Vec2D(0.15, 0.15)
        self.radius = 5
        self.color = (255, 255, 255)

    def reset(self):
        self.velocity = Vec2D(0.15, 0.15).rotate(random.randint(0, 360))
        self.position = Vec2D(width / 2, height / 2)

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, value):
        self.position = Vec2D(value, self.position[1])

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position = Vec2D(self.position[0], value)

    @property
    def vx(self):
        return self.velocity[0]

    @vx.setter
    def vx(self, value):
        self.velocity = Vec2D(value, self.velocity[1])

    @property
    def vy(self):
        return self.velocity[1]

    @vy.setter
    def vy(self, value):
        self.velocity = Vec2D(self.velocity[0], value)

    @property
    def speed(self):
        return abs(self.velocity)

    def intersects(self, rect):
        rx, ry = rect.center
        rw, rh = rect.size

        dist_x = abs(self.x - rx)
        dist_y = abs(self.y - ry)

        if dist_x > rw / 2.0 + self.radius or dist_y > rh / 2.0 + self.radius:
            return False

        if dist_x <= rw / 2.0 or dist_y <= rh / 2.0:
            return True

        cx = dist_x - rw / 2.0
        cy = dist_y - rh / 2.0

        c_sq = cx ** 2.0 + cy ** 2.0

        return c_sq <= self.radius ** 2.0

    def update(self, delta, left_player, right_player):
        global width

        self.position += self.velocity * delta

        if (self.x < 50 and self.vx < 0) or (self.x > width - 50 and self.vx > 0):
            for item in [left_player, right_player]:
                if self.intersects(item):
                    item.success()

                    cx, cy = item.center
                    w, h = item.size
                    relative_y = (cy - self.y) / (h / 2)

                    speed = self.speed + (abs(relative_y) / 4)

                    angle = relative_y * 5 * (math.pi / 12)

                    if self.x > width / 2:
                        self.x = item.position.x - self.radius
                        self.velocity = Vec2D(
                            speed * -math.cos(angle),
                            speed * -math.sin(angle))
                    else:
                        self.x = item.position.x + item.width + self.radius
                        self.velocity = Vec2D(
                            speed * math.cos(angle),
                            speed * -math.sin(angle))

        if self.x - self.radius < 0 and self.vx < 0:
            left_player.fail()
            self.reset()

        elif self.x + self.radius > width and self.vx > 0:
            right_player.fail()
            self.reset()

        if self.y - self.radius < 0 and self.vy < 0:
            self.y = self.radius
            self.vy *= -1

        elif self.y + self.radius > height and self.vy > 0:
            self.y = height - self.radius
            self.vy *= -1

    def render(self, screen):
        draw.ellipse((
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius),
            self.color)


class Player():
    def __init__(self, side):
        global width, height

        self.score = 0
        self.y = height / 2
        self.next_y = self.y

        if side == 0:  # Left
            self.x = 25
        else:
            self.x = width - 25

        self.width = 5
        self.height = 50

    def paddle(self, y):
        self.next_y = y

    def success(self):
        self.score += 1

    def fail(self):
        self.score -= 1

    @property
    def center(self):
        return Position(
            x=self.x,
            y=self.y)

    @property
    def position(self):
        return Position(
            x=self.x - (self.width / 2),
            y=self.y - (self.height / 2))

    @property
    def size(self):
        return Size(
            w=self.width,
            h=self.height)

    def update(self):
        self.y = self.next_y

    def render(self, draw):
        draw.rectangle((self.x - (self.width / 2),
                        self.y - (self.height / 2),
                        self.x + (self.width / 2),
                        self.y + (self.height / 2)), (255, 255, 255))


player_one = Player(0)
player_two = Player(1)
ball = Ball()

time_last = millis()

player_one_pos = height / 2
player_two_pos = height / 2

displayhatmini.set_led(0, 0, 0)

paddle_speed = 15

while True:
    time_now = millis()
    time_delta = time_now - time_last

    player_one_pos = player_one.center.y
    if displayhatmini.read_button(displayhatmini.BUTTON_A):
        player_one_pos -= paddle_speed
    if displayhatmini.read_button(displayhatmini.BUTTON_B):
        player_one_pos += paddle_speed

    player_two_pos = player_two.center.y
    if displayhatmini.read_button(displayhatmini.BUTTON_X):
        player_two_pos -= paddle_speed
    if displayhatmini.read_button(displayhatmini.BUTTON_Y):
        player_two_pos += paddle_speed

    if player_one_pos < 0:
        player_one_pos = 0
    elif player_one_pos > height:
        player_one_pos = height

    if player_two_pos < 0:
        player_two_pos = 0
    elif player_two_pos > height:
        player_two_pos = height

    player_one.paddle(player_one_pos)
    player_two.paddle(player_two_pos)

    draw.rectangle((0, 0, width, height), (0, 0, 0))

    draw.rectangle((
        (width / 2) - 1,
        20,
        (width / 2) + 1,
        height - 20),
        (64, 64, 64))

    text(draw, "{0:02d}".format(player_one.score), (25, 25), 15, (255, 255, 255))
    text(draw, "{0:02d}".format(player_two.score), (width - 25, 25), 15, (255, 255, 255))

    player_one.update()
    player_two.update()
    ball.update(time_delta, player_one, player_two)

    ball.render(draw)
    player_one.render(draw)
    player_two.render(draw)

    displayhatmini.display()

    time.sleep(0.001)
    time_last = time_now
