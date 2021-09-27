from board import *
import busio, terminalio, displayio, time
from adafruit_displayio_sh1107 import SH1107
from adafruit_display_text import label

displayio.release_displays()
spi = busio.SPI(clock=GP10 ,MOSI=GP11)
display_bus = displayio.FourWire(spi, command=GP8, chip_select=GP9, reset=GP12)
display = SH1107(display_bus, width = 128, height =64)

splash = displayio.Group()
display.show(splash)

text_group = displayio.Group(scale = 2, x = 0, y = 6)
#text group、表示させるもの?

text = "GAIN:"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text
splash.append(text_group)

text2 = "HIGH"
text_group = displayio.Group(scale = 2, x = 60, y = 6)
text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFF00)
text_group.append(text_area2)  # Subgroup for text
splash.append(text_group)