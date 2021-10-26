#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
from ST7789 import ST7789

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
    from PIL import Image, ImageDraw, ImageFont

    print("PongTest")

    import random
    import time
    import math
    from collections import namedtuple
    from turtle import Vec2D


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
            self.position = Vec2D(width/2, height/2)
            self.velocity = Vec2D(0.15,0.15)
            self.radius = 5
            self.color = (255, 255, 255)

        def reset(self):
            self.velocity = Vec2D(0.15,0.15).rotate(random.randint(0, 360))
            self.position = Vec2D(width/2, height/2)

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

            if dist_x > rw/2.0+self.radius or dist_y > rh/2.0+self.radius:
                return False

            if dist_x <= rw/2.0 or dist_y <= rh/2.0:
                return True

            cx = dist_x-rw/2.0
            cy = dist_y-rh/2.0

            c_sq = cx**2.0 + cy**2.0

            return c_sq <= self.radius**2.0

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

                        speed = self.speed + (abs(relative_y)/4)

                        angle = relative_y * 5 * (math.pi / 12)
                        
                        if self.x > width/2:
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
            self.y = height/2
            self.next_y = self.y

            if side == 0: # Left
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
                x=self.x - (self.width/2),
                y=self.y - (self.height/2))

        @property
        def size(self):
            return Size(
                w=self.width,
                h=self.height)

        def update(self):
            self.y = self.next_y

        def render(self, draw):
            draw.rectangle((self.x - (self.width/2),
                            self.y - (self.height/2),
                            self.x + (self.width/2),
                            self.y + (self.height/2)), (255, 255, 255))


    player_one = Player(0)
    player_two = Player(1)
    ball = Ball()

    time_last = millis()

    player_one_pos = height/2
    player_two_pos = height/2

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
#
        draw.rectangle((0, 0, width, height), (0, 0, 0))

        draw.rectangle((
            (width/2) - 1,
            20,
            (width/2) + 1,
            height-20),
            (64, 64, 64))

        text(draw, "{0:02d}".format(player_one.score), (25, 25), 15, (255, 255, 255))
        text(draw, "{0:02d}".format(player_two.score), (width-25, 25), 15, (255, 255, 255))
        
        player_one.update()
        player_two.update()
        ball.update(time_delta, player_one, player_two)

        ball.render(draw)
        player_one.render(draw)
        player_two.render(draw)

        displayhatmini.display()

        time.sleep(0.001)
        time_last = time_now


    exit



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
