"""TinyOLED Desktop — I2C Bus Scanner"""
import subprocess
from core.framebuffer import Framebuffer

class I2CScanApp:
    NAME="i2c"; LABEL="I2C"; ICON="i2c"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.devices=[]; self._scanning=False; self.scan()
    def scan(self):
        self.devices=[]
        try:
            out=subprocess.check_output(["i2cdetect","-y","1"],text=True,stderr=subprocess.DEVNULL)
            for line in out.split("\n")[1:]:
                parts=line.split(":"); 
                if len(parts)<2: continue
                for token in parts[1].split():
                    if token!="--" and len(token)==2:
                        try: self.devices.append(int(token,16))
                        except: pass
        except: pass
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self.scan()
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("i2c",1,10); fb.text(f"I2C ({len(self.devices)} cihaz)",12,10)
        fb.hline(0,18,128)
        # 8x16 grid olarak adres tablosu
        for row in range(8):
            for col in range(16):
                addr=row*16+col; x=col*8; y=20+row*5
                if addr in self.devices:
                    fb.rect(x,y,7,4,fill=True)
                else:
                    fb.pixel(x+3,y+2)
        fb.text("[SEL] Tara",2,56); fb.text("LONG:geri",75,56)
