"""TinyOLED Desktop — Ay Evresi Göstergesi"""
import math, time
from core.framebuffer import Framebuffer
NAMES=["Yeni Ay","Hilal","Ilk Dordun","Siskin","Dolunay","Siskin","Son Dordun","Hilal"]

class MoonApp:
    NAME="moon"; LABEL="Ay"; ICON="moon"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.phase=0.0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): pass
    def on_long(self): self.on_exit()
    def update(self):
        ref=947182800; synodic=29.53058867
        self.phase=((time.time()-ref)/86400%synodic)/synodic
    def draw(self, fb: Framebuffer):
        fb.text("Ay Evresi",30,2)
        cx,cy,r=40,36,16; fb.circle(cx,cy,r,fill=True)
        illum=self.phase*2 if self.phase<=0.5 else (1-self.phase)*2
        for dy in range(-r,r+1):
            hw=int(math.sqrt(max(0,r*r-dy*dy))); sw=int(hw*(1-illum))
            if self.phase<=0.5:
                for sx in range(-hw,-hw+sw): fb.pixel(cx+sx,cy+dy,on=False)
            else:
                for sx in range(hw-sw,hw+1): fb.pixel(cx+sx,cy+dy,on=False)
        fb.circle(cx,cy,r)
        idx=int(self.phase*8)%8; fb.text(NAMES[idx],65,28)
        fb.text(f"%{illum*100:.0f} aydinlik",65,40)
        fb.text(f"Gun:{self.phase*29.53:.1f}/29.5",65,52)
