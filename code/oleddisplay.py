class oledDisplay:
    def __init__(self,sda=4,scl=5,title='oledtemp',screenTimeOut=180):
        self.scl = scl
        self.sda = sda
        self.display = ""
        self.title = title
        self.startupText = 'Configuring...'
        self.screenTime = 0
        self.screenTimeLimit = screenTimeOut
    
    def initDisplay(self):
        from machine import I2C
        from machine import Pin
        import ssd1306
        import writer
        import freesans20
        self.i2c = I2C(sda=Pin(self.sda),scl=Pin(self.scl))
        if 60 not in self.i2c.scan():
            raise RuntimeError('Cannot find display')
        self.display = ssd1306.SSD1306_I2C(128,64, self.i2c)
        self.freesans20 = writer.Writer(self.display,freesans20)

    def printFreeSans20(self,text,start=0,width=128,hzJustification='center',padding=0,top=30):
        if hzJustification == 'center':
            textlen=self.freesans20.stringlen(text)
            self.freesans20.set_textpos(((start+(width-textlen))//2)+padding,top)
            self.freesans20.printstring(text)
        elif hzJustification == 'left':
            self.freesans20.set_textpos(start+padding,top)
            self.freesans20.printstring(text)
        elif hzJustification == 'right':
            textlen=self.freesans20.stringlen(text)
            self.freesans20.set_textpost((width-textlen)-padding,top)
            self.freesans20.printstring(text)


    def startupDisplay(self):
        self.display.text(self.title,5,0,1)
        self.centerFreeSans20(self.startupText)
        self.display.show()
        
    def displayOff(self):
        self.displayEnabled=False
        self.display.poweroff()
        print('[ INFO]: oled Display Turned Off')
    
    def displayOn(self):
        self.displayEnabled=True
        self.display.poweron()
        print('[ INFO]: oled Display Turned On')
    
    def loadImage(self,filename):
        import framebuf
        with open(filename, 'rb') as f:
            f.readline()
            f.readline()
            width, height = [int(v) for v in f.readline().split()]
            data = bytearray(f.read())
        return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)
    
    def mainDisplay(self,temp,rh,ip,units):
        tempImage=self.loadImage('fahrenheit.pbm') if units=='imperial' else self.loadImage('celsius.pbm')
        rhImage=self.loadImage('percent.pbm')
        if self.display:
            self.display.fill(0)
            self.display.rect(0,29,64,64,1)
            self.display.blit(tempImage,28,52)
            self.display.blit(rhImage,92,52)
            self.display.text(self.title,5,0,1)
            self.display.text(ip,5,16,1)
            self.printFreeSans20(temp,0,64,'center',0,30)
            self.printFreeSans20(rh,64,64,'center',0,30)
            self.display.show()