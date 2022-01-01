class Net:
    def __init__(self):
        from network import WLAN
        from network import STA_IF
        self.wlanStation = WLAN(STA_IF)
        self.ntpCountLimit = 5
        self.stationIp = ""

    def initStation(self,ssid,ssidPass):
        if not self.wlanStation.isconnected():
            self.wlanStation.active(True)
            self.wlanStation.connect(ssid,ssidPass)
            while not self.wlanStation.isconnected():
                pass
        self.stationIp = str(self.wlanStation.ifconfig()[0])
    
    def ntpSyncTime(self):
        from machine import RTC
        from time import sleep
        import ntptime
        rtc = RTC()
        self.ntpCount = 1
        while self.ntpCount <= self.ntpCountLimit:
            print("[ INFO]: NTP Time Sync Attempt #%i/%i"%(self.ntpCount,self.ntpCountLimit))
            self.ntpCount+=1
            ntptime.settime()
            print('[ INFO]: %s'%str(rtc.datetime()[0]))
            if 2020 < rtc.datetime()[0]:
                self.ntpCount=self.ntpCountLimit+1
            sleep(1)
            self.ntpCount += 1
        print('[ INFO]: NTP set RTC to: %i/%i/%i %i:%i:%i GMT'%(rtc.datetime()[0],rtc.datetime()[1],rtc.datetime()[2],rtc.datetime()[3],rtc.datetime()[4],rtc.datetime()[5]))