"""TinyOLED Desktop — Dijital Pusula"""
import math, time
from core.framebuffer import Framebuffer

class CompassApp:
    NAME="compass"; LABEL="Pusla"; ICON="compass"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.heading=0.0; self._last=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self._read()
    def on_long(self): self.on_exit()
    def _read(self):
        try:
            import smbus2; bus=smbus2.SMBus(1); addr=0x1E
            x=bus.read_word_data(addr,0x03); z=bus.read_word_data(addr,0x05); y=bus.read_word_data(addr,0x07)
            self.heading=math.degrees(math.atan2(y,x))%360; bus.close()
        except:
            self.heading=(self.heading+__import__("random").uniform(-5,5))%360
    def update(self):
        now=time.monotonic()
        if now-self._last<0.5: return
        self._last=now; self._read()
    def draw(self, fb: Framebuffer):
        fb.text("Pusula",45,2)
        cx,cy,r=64,36,22
        fb.circle(cx,cy,r)
        dirs={"N":0,"D":90,"G":180,"B":270}
        for label,deg in dirs.items():
            rad=math.radians(deg-self.heading-90)
            tx=int(cx+(r+5)*math.cos(rad)); ty=int(cy+(r+5)*math.sin(rad))
            fb.text(label,tx-2,ty-3)
        # İbre (her zaman yukarı gösterir, kadran döner)
        rad=math.radians(-90)
        nx=int(cx+(r-4)*math.cos(rad)); ny=int(cy+(r-4)*math.sin(rad))
        fb.line(cx,cy,nx,ny)
        fb.circle(cx,cy,2,fill=True)
        fb.text(f"{int(self.heading)}°",95,30)
