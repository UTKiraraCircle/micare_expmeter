import math, time, adafruit_tsl2591
from board import *
from busio import I2C

i2c = I2C(GP27,GP26)
TSL_addr = 0x29
sensor = adafruit_tsl2591.TSL2591(i2c, address = TSL_addr)
sensor.gain = adafruit_tsl2591.GAIN_LOW
k = 0
while k<4:
    Ev = math.log(float(sensor.lux)/2.5,2)
    time.sleep(0.1)
    k += 1
if Ev < 2:
    sensor.gain = adafruit_tsl2591.GAIN_MAX
elif Ev < 6.7:
    sensor.gain = adafruit_tsl2591.GAIN_HIGH
elif Ev <10:
    sensor.gain = adafruit_tsl2591.GAIN_MED
gainlist = ['LW','MD','HI','MX']
k = 0
while k<4:
    Ev = math.log(float(sensor.lux)/2.5,2)
    time.sleep(0.1)
    k += 1
print(Ev)
print(gainlist[int(sensor.gain/16)])