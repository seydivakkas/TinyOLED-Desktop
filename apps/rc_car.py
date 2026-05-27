"""TinyOLED Desktop — Robot Araba Kumandası"""
from core.framebuffer import Framebuffer

DIRS=["ILERI","GERI","SOL","SAG","DUR"]

class RCCarApp:
    NAME="rc_car"; LABEL="Araba"; ICON="car"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.dir_idx=4; self.speed=50
    def on_up(self): self.dir_idx=(self.dir_idx-1)%len(DIRS)
    def on_down(self): self.dir_idx=(self.dir_idx+1)%len(DIRS)
    def on_sel(self):
        # L298N motor sürücü komutları
        try:
            import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM)
            # Motor A: GPIO 23,24; Motor B: GPIO 5,6; Enable: GPIO 12,13
            pass
        except: pass
    def on_long(self): self.dir_idx=4; self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("car",1,10); fb.text("RC Kumanda",12,10); fb.hline(0,18,128)
        cx,cy=64,40
        # Yön okları
        fb.text("^",cx-2,cy-16); fb.text("v",cx-2,cy+10)
        fb.text("<",cx-20,cy-3); fb.text(">",cx+16,cy-3)
        d=DIRS[self.dir_idx]
        fb.text_centered(d,cy-3)
        fb.rect(cx-12,cy-6,24,12,fill=(d!="DUR"))
        fb.text(f"Hiz: %{self.speed}",2,56)
