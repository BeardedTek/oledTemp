# CONFIG (defaults)
ssid="Your SSID"
ssidPass = "Your SSID Password"
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