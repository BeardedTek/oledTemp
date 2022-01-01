class sensor:
    def __init__(self):
        self.sensorType = 'dht11'
        self.units = 'imperial'
        self.temp = -1
        self.rh = -1
        self.lastTemp = 0
        self.lastRH = 0
        self.temp = 0
        self.rh = 0
    
    def getDHT11(self,pin):
        import dht
        from machine import Pin
        self.dht11 = dht.DHT11(Pin(pin))
        self.dht11.measure()
        self.temp = self.dht11.temperature()
        if self.units=='imperial':
            self.temp = self.temp * 9 / 5 + 32
        self.rh = self.dht11.humidity()

    def getButton(self,pin):
        from machine import Pin
        self.button = Pin(pin,Pin.IN)
        self.buttonValue = self.button.value()
        if self.buttonValue == 1:
            return True
        else:
            return False
