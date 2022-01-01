# CONFIG (defaults)
ssid="I'm Not Gonna Tell You"
ssidPass = "MegLogWillEmb7040"
interval=3
title="office"
dht=14
btn=12
sda=4
scl=5
timeout=30

from loop import oledTemp
oledtemp = oledTemp(ssid,ssidPass,interval,title,dht,btn,sda,scl,timeout)
oledtemp.start()