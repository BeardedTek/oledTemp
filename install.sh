#!/bin/bash
PORT="/dev/ttyUSB0"
FLASHBAUD="460800"
REPLBAUD="115200"
ESP="esp8266"
FIRMWARE="./firmware/$ESP-20210902-v1.17.bin"
esptool.py --port $PORT erase_flash
esptool.py --port $PORT --baud $FLASHBAUD write_flash --flash_size=detect 0 $FIRMWARE
for FILE in ./code/*
do 
    echo Uploading $FILE to $ESP on $PORT
    ampy --port $PORT --baud $REPLBAUD put $FILE
done
picocom $PORT -b$REPLBAUD
