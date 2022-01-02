import config






from loop import oledTemp
oledtemp = oledTemp(config.ssid,config.ssidPass,config.interval,config.title,config.dht,config.btn,config.sda,config.scl,config.timeout)
oledtemp.start()