class sensor:
    def __init__(self):
        self.sensorType = 'dht11'
        self.units = imperial
        self.temp = -1
        self.rh = -1
        self.lastTemp = 0
        self.lastRH = 0
    
    def getDHT11(self,pin):
        from dht import DHT
        from machine import Pin
        self.dht11 = DHT(Pin(pin))
        self.dht11.measure()
        self.temp = self.dht11.temperature()
        if self.units=='imperial':
            self.temp = self.temp*9//5+32
        self.rh = self.dht11.humidity()

    def getButton(self,pin):
        self.button = Pin(12,Pin.IN)
        self.buttonValue = self.button.value()
        if self.buttonValue == 1:
            return True
        else:
            return False
