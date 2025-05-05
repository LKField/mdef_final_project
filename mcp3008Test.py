"""

This code is directly Romilly on GitHub under a MIT License and can be found at:
from https://github.com/romilly/pico-code/blob/master/src/pico_code/pico/mcp3008/mcp3008-demo.py
"""

from time import sleep
from mcp3008 import MCP3008
from machine import Pin

spi = machine.SPI(0, sck=Pin(2),mosi=Pin(3),miso=Pin(4), baudrate=100000)
cs = machine.Pin(22, machine.Pin.OUT)


chip = MCP3008(spi, cs)

while True:
    print(chip.read(0))
    sleep(1)