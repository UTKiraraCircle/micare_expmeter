import math, time, adafruit_tsl2591, terminalio, displayio
from board import *
from busio import I2C, SPI
from adafruit_displayio_sh1107 import SH1107
from adafruit_display_text import label
i2c = I2C(GP27,GP26)
sensor = adafruit_tsl2591.TSL2591(i2c, address = 0x29)
displayio.release_displays()
spi = SPI(clock = GP10, MOSI = GP11)
display_bus = displayio.FourWire(spi, command = GP8, chip_select = GP9, reset = GP12)
display = SH1107(display_bus ,width = 128,height = 64)
gainlist = ['LOW ','MED ','HIGH','MAX ']
Tlist = ['1', '1/2', '1/4', '1/8', '1/15', '1/30', '1/60', '1/125', '1/250', '1/500', '1/1000', '1/2000', '1/4000']
while True:
    sensor.gain = adafruit_tsl2591.GAIN_LOW
    k = 0
    while k < 4:
        Ev = math.log(float(sensor.lux)/2.5, 2)
        if Ev < 1.5:
            sensor.gain = adafruit_tsl2591.GAIN_MED
            Ev = math.log(float(sensor.lux)/2.5, 2)
            break
        time.sleep(0.1)
        k += 1
    if Ev < 2.3:
        sensor.gain = adafruit_tsl2591.GAIN_MAX
    elif Ev < 6.5:
        sensor.gain = adafruit_tsl2591.GAIN_HIGH
    elif Ev < 9:
        sensor.gain = adafruit_tsl2591.GAIN_MED
    else:
        sensor.gain = adafruit_tsl2591.GAIN_LOW
    gain = gainlist[int(sensor.gain/16)]
    k = 0
    while k < 5:
        Ev = math.log(float(sensor.lux)/2.5,2)
        time.sleep(0.1)
        k += 1
    Ev1 = Ev + 2 #+は実地試験の結果を鑑みて補正
    splash = displayio.Group()
    text_group = displayio.Group(scale = 1, x = 1, y = 3)
    text = "GAIN:" + gain + " Ev:" + str(Ev1)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
    text_group.append(text_area)
    splash.append(text_group)
    for N in range(3): #ISO400までを表示して視認性向上を図る
        Ev2 = Ev1 + N
        #FBをもとに露出計算部分を改修
        if Ev2 < 4:
            Av = 2
            Tv = Ev2 - 2
            T = str(round(2**(-Tv),1))
        else:
            Tv = math.ceil(Ev2/2)
            T = Tlist[Tv]
            Av = Ev2 - Tv
        Araw = 2**(Av/2)
        if Araw//10 == 0:
            A = math.floor(10*Araw)/10
        else:
            A = math.floor(Araw)
        Exp =str(A) + " " + T
        text_group=displayio.Group(scale = 2, x = 1, y = int(15 + 17 * N))
        text_area = label.Label(terminalio.FONT,text=Exp,color=0xFFFF00)
        text_group.append(text_area)
        splash.append(text_group)
    display.show(splash)