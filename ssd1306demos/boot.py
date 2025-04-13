from machine import Pin,I2C,SoftI2C,freq
from ssd1306fbi import SSD1306_I2C
from os import mount,listdir,umount
from time import sleep
freq(240000000) # set the CPU frequency to 240 MHz

i2c=SoftI2C(scl=Pin(22), sda=Pin(21))

# Screen constant
WIDTH = const(128)
HEIGHT = const(64)
LINE_HEIGHT = const(8)

# create the display
o=SSD1306_I2C(WIDTH,HEIGHT,i2c)

