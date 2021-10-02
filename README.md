# micare_expmeter
micare vol.1 に寄稿した記事「もゆもゆに露出計を捧ぐ」で製作した露出計の使用素材・掲載ソースコードの注釈など

## 今回の製作にあたって使用したハード・ソフトのマテリアル
### 素子
* Raspberry Pi Pico
* [Seeed Studio Raspberry Pi Pico用 OLEDディスプレイモジュール【103030401】](https://www.marutsu.co.jp/pc/i/2223782/)
  * ドライバICは SH1107
  * ほかにcircuitpythonのライブラリが確認できた電子ペーパー・LCD/OLEDディスプレイのドライバICは以下の通り
    * IL0398
    * SH1106
    * SH1107
    * SSD1305
    * SSD1306
    * SSD1325
    * SSD1327
* Adafruit TSL2591 光センサモジュール
* 【warning】今回は複数のI2Cスレーブデバイスを同じI2Cバスに繋ぐことができなかったため、光センサをI2C通信、OLEDをSPI通信で駆動した
### 配線部品・電源
* ピンヘッダ
  * 両端ロングが望ましい
* メス―メスジャンパワイヤ
* 熱収縮チューブφ1.5
  * φ2が望ましいと思われる
* はんだ線
* 単4乾電池*2
* 同電池ボックス
* 1回路1接点トグルスイッチ
* ほかに試作段階で ブレッドボード オス―オスジャンパワイヤ を使用
### 開発言語
* circuitpython 6.3.0
### 開発環境
* Thonny ver 1.1.16, 1.1.17

## 掲載ソースコードの注釈
* README.md このファイル
* blink_LED.py オンボードLEDを用いたLチカ マイコンの動作確認用
* ExpMeter_Sensor.py 感度の自動設定のためのコード 試作段階で生えたもの
* **code_final_with_comments.py 2021 9/27 時点で最新のコード コメントつき**
* **code_final_WITHOUT_comments.py 2021 9/27 時点で最新のコード コメントなし**

## stlファイルの注釈
* 露出計本体.stl シューの形状はPENTAX SPのアクセサリシューに合わせた PENTAX KPには嵌ったが、PENTAX KMのシューに嵌めるにはやすりによる加工が必要だった。予め取り付け先の形状を測定することを勧める
* 廂.stl 光センサ部分の側面からの光の入射を防ぐ廂 ネジは2mm径のものがよい
* 側面蓋.stl 露出計を入れた後、側面に蓋をする部品 もう少し固定部分に遊びがあっても良かったかもしれない
