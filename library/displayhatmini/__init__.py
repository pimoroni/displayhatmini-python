import RPi.GPIO as GPIO
from ST7789 import ST7789


__version__ = '0.0.2'


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

    def __init__(self, buffer, backlight_pwm=False):
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

        if backlight_pwm:
            GPIO.setup(self.BACKLIGHT, GPIO.OUT)
            self.backlight_pwm = GPIO.PWM(self.BACKLIGHT, 500)
            self.backlight_pwm.start(100)
        else:
            self.backlight_pwm = None

        self.st7789 = ST7789(
            port=self.SPI_PORT,
            cs=self.SPI_CS,
            dc=self.SPI_DC,
            backlight=None if backlight_pwm else self.BACKLIGHT,
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

    def set_backlight(self, value):
        if self.backlight_pwm is not None:
            self.backlight_pwm.ChangeDutyCycle(value * 100)
        else:
            self.st7789.set_backlight(int(value))

    def on_button_pressed(self, callback):
        for pin in (self.BUTTON_A, self.BUTTON_B, self.BUTTON_X, self.BUTTON_Y):
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=callback)

    def read_button(self, pin):
        return not GPIO.input(pin)

    def display(self):
        self.st7789.display(self.buffer)
