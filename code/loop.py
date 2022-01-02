class oledTemp:
    def __init__(self,ssid,ssidPass,interval=30,title="main",dht=14,btn=12,sda=4,scl=5,timeout=180):
        self.updateInterval = interval
        self.server = "192.168.2.245"
        self.title = title
        self.dht = dht
        self.btn = btn
        self.sda = sda
        self.scl = scl
        self.ssid = ssid
        self.ssidPass = ssidPass
        self.screenOn = True
        self.screenTimeout = timeout
        self.dhtRead = False
        self.init = True
    
    def start(self):
        import time
        from oleddisplay import oledDisplay
        from sensors import sensor
        from mqtt import MQTT
        from net import Net
        wlan = Net()
        wlan.initStation(self.ssid,self.ssidPass)
        wlan.ntpSyncTime()
        oled = oledDisplay(self.sda,self.scl,self.title,self.screenTimeout)
        oled.initDisplay()
        oled.startupDisplay()
        oled.screenTime = time.time()
        sensors = sensor()
        self.lastTime = time.time()
        temperature=0
        humidity=0
        while True:
            #try:
                self.curTime = time.time()
                #print('[DEBUG]: screenTime: %s, curTime: %s, screenTimeLimit: %s'%(oled.screenTime,self.curTime,oled.screenTimeLimit))
                if oled.screenTime < self.curTime - oled.screenTimeLimit:
                    oled.screenTime = self.curTime
                    if self.screenOn:
                        oled.displayOff()
                        self.screenOn=False
                if sensors.getButton(self.btn):
                    #print("[ INFO]: Button Pressed")
                    if self.screenOn:
                        oled.displayOff()
                        self.screenOn=False
                    else:
                        oled.displayOn()
                        self.screenOn=True

                timeout = self.lastTime + self.updateInterval
                #print('[DEBUG]: timeout: %s, curTime: %s '%(timeout,self.curTime))
                if timeout < self.curTime or self.init:
                    if self.init:
                        self.init = False
                    self.lastTime = self.curTime
                    while not self.dhtRead:
                        try:
                            sensors.getDHT11(self.dht)
                            temperature = sensors.temp
                            humidity = sensors.rh
                            #print("[ INFO][dht11]: temp: %s, rh: %s"%(str(temperature),str(humidity)))
                            self.dhtRead = True
                        except:
                            print("[ERROR]: Can't Read DHT, Retrying")
                            self.dhtRead = False
                        time.sleep(2)
                    #try:
                    if temperature != -1 and humidity != -1:
                        self.systemInit = False
                        mqtt = MQTT(self.server)
                        mqtt.connect()
                        mqtt.publish(temperature,humidity,wlan.stationIp,self.curTime,self.title)
                    #except:
                    #    print("[ERROR][LOOP/MQTT]")
                    #print("[ INFO]: temp: %s, rh: %s"%(str(temperature),str(humidity)))
                    if temperature != sensors.lastTemp or humidity != sensors.lastRH:
                        oled.mainDisplay(temperature,humidity,wlan.stationIp,sensors.units)
                        sensors.lastTemp = temperature
                        sensors.lastRH = humidity
                    output = "[ INFO]: {}{}F | {}%RH".format(temperature,chr(176),humidity)
                    print('[ INFO]: %s'%output)
                time.sleep(0.15)