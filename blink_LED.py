import digitalio
from board import *
import time

led = digitalio.DigitalInOut(GP25)
led.direction = digitalio.Direction.OUTPUT
while True:
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)