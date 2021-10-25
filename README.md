# {{TITLE}}

[![Build Status](https://travis-ci.com/pimoroni/{{LIBNAME}}-python.svg?branch=master)](https://travis-ci.com/pimoroni/{{LIBNAME}}-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/{{LIBNAME}}-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/{{LIBNAME}}-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/{{LIBNAME}}.svg)](https://pypi.python.org/pypi/{{LIBNAME}})
[![Python Versions](https://img.shields.io/pypi/pyversions/{{LIBNAME}}.svg)](https://pypi.python.org/pypi/{{LIBNAME}})

# Pre-requisites

You must enable (delete where appropriate):

* i2c: `sudo raspi-config nonint do_i2c 0`
* spi: `sudo raspi-config nonint do_spi 0`

You can optionally run `sudo raspi-config` or the graphical Raspberry Pi Configuration UI to enable interfaces.

# Installing

Stable library from PyPi:

* Just run `pip3 install {{LIBNAME}}`

In some cases you may need to use `sudo` or install pip with: `sudo apt install python3-pip`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/{{LIBNAME}}-python`
* `cd {{LIBNAME}}-python`
* `sudo ./install.sh`

