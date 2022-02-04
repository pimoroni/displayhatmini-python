# Display HAT Mini

[![Build Status](https://shields.io/github/workflow/status/pimoroni/displayhatmini-python/Python%20Tests.svg)](https://github.com/pimoroni/displayhatmini-python/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/displayhatmini-python/badge.svg?branch=main)](https://coveralls.io/github/pimoroni/displayhatmini-python?branch=main)
[![PyPi Package](https://img.shields.io/pypi/v/displayhatmini.svg)](https://pypi.python.org/pypi/displayhatmini)
[![Python Versions](https://img.shields.io/pypi/pyversions/displayhatmini.svg)](https://pypi.python.org/pypi/displayhatmini)

# Pre-requisites

You must enable:

* spi: `sudo raspi-config nonint do_spi 0`

You can optionally run `sudo raspi-config` or the graphical Raspberry Pi Configuration UI to enable interfaces.

# Installing

Stable library from PyPi:

* Just run `pip3 install displayhatmini`

In some cases you may need to use `sudo` or install pip with: `sudo apt install python3-pip`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/displayhatmini-python`
* `cd displayhatmini-python`
* `sudo ./install.sh`

# Useful Links

* Pinout - https://pinout.xyz/pinout/display_hat_mini
* Buy - https://shop.pimoroni.com/products/display-hat-mini
# Changelog
0.0.2
-----

* Add PWM backlight support (not super stable, but it works)
* Add `on_button_pressed` for interrupt driven buttons

0.0.1
-----

* Initial Release
