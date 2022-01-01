# CONFIG (defaults)
interval=30
title="main"
dht=14
btn=12
sda=4
scl=5
from loop import oledTemp
oledtemp = oledTemp(interval,title,dht,btn,sda,scl)
oledtemp.start()