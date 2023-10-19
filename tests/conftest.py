import sys

import mock
import pytest


@pytest.fixture(scope='function', autouse=False)
def GPIO():
    """Mock RPi.GPIO module."""
    GPIO = mock.MagicMock()
    # Fudge for Python < 37 (possibly earlier)
    sys.modules['RPi'] = mock.MagicMock()
    sys.modules['RPi'].GPIO = GPIO
    sys.modules['RPi.GPIO'] = GPIO
    yield GPIO
    del sys.modules['RPi']
    del sys.modules['RPi.GPIO']


@pytest.fixture(scope='function', autouse=False)
def ST7789(PIL):
    """Mock ST7789 module."""
    ST7789 = mock.MagicMock()
    sys.modules['ST7789'] = ST7789
    yield ST7789
    del sys.modules['ST7789']


@pytest.fixture(scope='function', autouse=False)
def displayhatmini():
    """Import Display HAT mini."""
    import displayhatmini
    yield displayhatmini
    del sys.modules['displayhatmini']


@pytest.fixture(scope='function', autouse=False)
def PIL():
    """Mock PIL module."""
    PIL = mock.MagicMock()
    sys.modules['PIL'] = PIL
    yield PIL
    del sys.modules['PIL']
