import mock


def test_setup(GPIO, ST7789, displayhatmini):
    display = displayhatmini.DisplayHATMini(bytearray())

    GPIO.setup.assert_has_calls((
        mock.call(display.BUTTON_A, GPIO.IN, pull_up_down=GPIO.PUD_UP),
        mock.call(display.BUTTON_B, GPIO.IN, pull_up_down=GPIO.PUD_UP),
        mock.call(display.BUTTON_X, GPIO.IN, pull_up_down=GPIO.PUD_UP),
        mock.call(display.BUTTON_Y, GPIO.IN, pull_up_down=GPIO.PUD_UP),

        mock.call(display.LED_R, GPIO.OUT)
        mock.call(display.LED_G, GPIO.OUT)
        mock.call(display.LED_B, GPIO.OUT)
    ))
