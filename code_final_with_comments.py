"""
個人使用 引用を付しての参照・言及可
For personal use, citation with reference approved.
商業的な二次配布禁止
Commercial secondary destribution prohibited.
実際にPicoに保存して動かす場合はファイル名を "code.py" とすること
You must rename this file when you use this file as a driver of your Pico. 
"""

# 必要なライブラリをインポート
import math, time, adafruit_tsl2591, terminalio, displayio
from board import *
from busio import I2C, SPI
from adafruit_displayio_sh1107 import SH1107
from adafruit_display_text import label

# 光センサ、ディスプレイを駆動するためのI2C、SPI通信を有効化 GP~はマイコンのピン指定
i2c = I2C(GP27,GP26)
sensor = adafruit_tsl2591.TSL2591(i2c, address = 0x29)
displayio.release_displays()
spi = SPI(clock = GP10, MOSI = GP11)
display_bus = displayio.FourWire(spi, command = GP8, chip_select = GP9, reset = GP12)
display = SH1107(display_bus ,width = 128,height = 64)

# ディスプレイに表示する文字列のうち内容が決まっているものを定義
gainlist = ['LOW ','MED ','HIGH','MAX ']
Tlist = ['1', '1/2', '1/4', '1/8', '1/15', '1/30', '1/60', '1/125', '1/250', '1/500', '1/1000', '1/2000', '1/4000']

# 電源が入っている間は以下の処理を無限に繰り返す
while True:
    # 最初は低感度に設定して強い光にも対応
    #初手でセンサ感度が高いとエラー処理が面倒なので低感度に設定
    sensor.gain = adafruit_tsl2591.GAIN_LOW
    k = 0
    while k < 4: # 測光してすぐの値は荒ぶるので4回目の測光値を感度調整に使用
        Ev = math.log(float(sensor.lux)/2.5, 2)
        # Pico用のcircuitpythonのmathモジュールにはどういうわけかlog2函数がないのでこれで代用
        if Ev < 1.5:
            #あまりに暗いと対数函数の真数0エラーを吐くのでwhileループ中でも早めに離脱させる
            sensor.gain = adafruit_tsl2591.GAIN_MED
            Ev = math.log(float(sensor.lux)/2.5, 2)
            break
        time.sleep(0.1)
        k += 1
    # 最初の値ごとに感度をあらためて設定
    if Ev < 2.3:
        sensor.gain = adafruit_tsl2591.GAIN_MAX
    elif Ev < 6.5:
        sensor.gain = adafruit_tsl2591.GAIN_HIGH
    elif Ev < 9:
        sensor.gain = adafruit_tsl2591.GAIN_MED
    else:
        sensor.gain = adafruit_tsl2591.GAIN_LOW
    # ここで使用するセンサ感度が決まるのでディスプレイの表示内容を決めておく
    gain = gainlist[int(sensor.gain/16)]
    
    # ディスプレイ表示に使う明るさを調整した感度で測光
    k = 0
    while k < 5:
        Ev = math.log(float(sensor.lux)/2.5,2)
        time.sleep(0.1)
        k += 1
    
    Ev1 = Ev + 2 # 実地試験の結果を鑑みて測光された露出を補正
    splash = displayio.Group() # splash...のあたりなんも理解していない JKすぷらっしゅ...?
    text_group = displayio.Group(scale = 1, x = 1, y = 3)
    # 1行目はユーザーが直接求める情報ではないので小さく表示
    text = "GAIN:" + gain + " Ev:" + str(Ev1) # 1行目の表示
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
    text_group.append(text_area)
    splash.append(text_group)
    
    #ISO400までの参考露出を計算して表示
    for N in range(3):
        Ev2 = Ev1 + N
        # フィードバックをもとに露出計算部分を改修
        if Ev2 < 4:
            Av = 2
            Tv = Ev2 - 2
            T = str(round(2**(-Tv),1)) #長いシャッタ―は秒数を直接表示
        else:
            # 明るい場合にシャッタースピードが小さく出るよう、Tvを切り上げ
            Tv = math.ceil(Ev2/2)
            T = Tlist[Tv]
            Av = Ev2 - Tv
        # 絞り値を計算
        Araw = 2**(Av/2)
        if Araw//10 == 0:
            A = math.floor(10*Araw)/10 # 10未満のF値は小数点以下第2位以降を切り捨て
        else:
            A = math.floor(Araw) # 10以上のF値は整数値で表示
        Exp =str(A) + " " + T # これが参考露出1行分 これを3回別のISO感度で繰り返す
        text_group=displayio.Group(scale = 2, x = 1, y = int(15 + 17 * N))
        text_area = label.Label(terminalio.FONT,text=Exp,color=0xFFFF00)
        text_group.append(text_area)
        splash.append(text_group)
    display.show(splash) #JKすぷらっしゅ
