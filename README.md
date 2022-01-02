# oledTemp
## v0.1.1 - Initial Release

## Hardware Config
- DHT11
  - Data Pin 14
  - 3.3v
  - Gnd
- Button
  - Pull up 10k resistor and 3.3V wired to one side
  - Other side Pin 12
- SSD1306
  - SDA Pin 4
  - SCL Pin 5
  - 3.3v
  - Gnd

## Install
### - Copy config_example.py to config.py and edit the variables therein to suit your needs

- esptool
  - pip3 install esptool
- ampy
  - pip3 install adafruit-ampy
- picocom
  - Debian/Ubuntu derivative
    - apt install picocom
  - Fedora
    - dnf install picocom
  - OpenSuse
    - zypper in picocom



install.sh
For use on an ESP8266 (I used a NodeMCU)
1) Erases Flash
2) Loads micropython 20210902-v1.17
3) Copies all files in the code directory to the ESP8266
4) Launch picocom

After picocom launches, press `Ctrl-D` to reset the ESP8266.
```
#!/bin/bash
PORT = "/dev/ttyUSB0"
FLASHBAUD = "460800"
REPLBAUD = "115200"
esptool.py --port $PORT erase_flash
esptool.py --port /dev/ttyUSB0 --baud $FLASHBAUD write_flash --flash_size=detect 0 ./firmware/esp8266-20210902-v1.17.bin
for FILE in ./code/*
do 
    echo Installing $FILE to ESP on $PORT
    ampy --port /dev/ttyUSB0 --baud $REPLBAUD put $FILE
done
picocom $PORT -b$REPLBAUD
```