class MQTT:
    def __init__(self,server):
        from ubinascii import hexlify
        from machine import unique_id
        self.mqttClientId = hexlify(unique_id())
        self.mqttServer = server
    
    def connect(self):
        from umqttsimple import MQTTClient
        self.mqttClient = MQTTClient(self.mqttClientId,self.mqttServer)
        self.mqttClient.connect()

    def publish(self,temp,rh,ip,mqttTime,mqttTitle):
        try:
            msgStr="{\"temperature\":%s,\"humidity\":%s,\"ip_address\":\"%s\",\"last_updated\":%s}"%(str(temp),str(rh),str(ip),str(mqttTime))
            msg = b'%s'%msgStr
            pub = 'oledtemp/%s'%mqttTitle
            self.mqttClient.publish(pub,msg)
            print('[ INFO]: %s: %s'%(pub,msg))
        except OSError as e:
            print('[ERROR]: %s'%str(e))
