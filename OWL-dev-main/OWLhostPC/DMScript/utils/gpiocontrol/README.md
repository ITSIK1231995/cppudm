## Python Library to Control GPIO on Hermes EVT Board

### Prerequisites

- [Python 2.7 (32-bit)](https://www.python.org/)
- [pyWin32](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/)

### Usage

```py
from gpio_ctrl import GPIOCtrl


gpio = GPIOCtrl('\\.\\COM3')
# Power on DUT
gpio.TurnOnPwr()
# Power off DUT
gpio.TurnOffPwr()
# Read GPIO Pins
gpio.ReadIO()
# Write to GPIO Pins
gpio.WriteIO(mask, value)
```