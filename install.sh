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