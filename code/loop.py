class oledTemp:
    def __init__(self,interval=30,title="main",dht=14,btn=12,sda=4,scl=5):
        self.updateInterval = interval
        self.server = "192.168.2.245"
        self.title = title
        self.dht = dht
        self.btn = btn
        self.sda = sda
        self.scl = scl
    
    def start(self):
        import time
        from oleddisplay import oledDisplay
        from sensors import sensor
        from mqtt import MQTT
        from net import Net
        wlan = Net()
        wlan.initStation()
        wlan.ntpSyncTime()
        oled = oledDisplay(self.sda,self.scl)
        oled.initDisplay()
        oled.startupDisplay()
        sensors = sensor()
        self.lastTime = time.time()
        while True:
            try:
                self.curTime = time.time()
                if oled.screenTime < self.curTime - oled.screenTimeLimit:
                    oled.screenTime = self.curTime
                    oled.displayOff()
                    if sensors.getButton(self.btn):
                        print("[ INFO]: Button Pressed")
                    timeout = self.lastTime + self.updateInterval
                    if timeout < self.curTime:
                        self.lastTime = self.curTime
                        try:
                            dht11 = sensors.getDHT11(self.dht)
                            temperature = dht11.temp
                            humidity = dht11.rh
                        except:
                            print("[ERROR]: Can't Read DHT")
                        if temperature != -1 and humidity != -1:
                            self.systemInit = False
                            wait = self.updateInterval
                            mqtt = MQTT(self.server)
                            mqtt.connect()
                            mqtt.publish(temperature,humidity,wlan.stationIp,self.curTime,self.title)
                        if temperature != sensors.lastTemp or humidity != sensors.lastRH:
                            oled.mainDisplay(temperature,humidity,wlan.stationIp,sensors.units)
                            sensors.lastTemp = temperature
                            sensors.lastRH = humidity
                        output = "[ INFO]: {}{}F | {}%RH".format(temperature,chr(176),humidity)
                        print(output)
            except Exception as exc:
                print('[ERROR] : %s'%exc)
            time.sleep(0.25)