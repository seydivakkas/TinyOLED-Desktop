"""TinyOLED Desktop — Starfield Ekran Koruyucu"""
import random, time
from core.framebuffer import Framebuffer

class StarfieldApp:
    NAME="starfield"; LABEL="Yldiz"; ICON="star"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.stars=[(random.uniform(-1,1),random.uniform(-1,1),random.uniform(0.1,1)) for _ in range(40)]
        self._last=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): pass
    def on_long(self): self.on_exit()
    def update(self):
        now=time.monotonic()
        if now-self._last<0.05: return
        self._last=now
        for i in range(len(self.stars)):
            x,y,z=self.stars[i]; z-=0.02
            if z<=0: self.stars[i]=(random.uniform(-1,1),random.uniform(-1,1),1.0)
            else: self.stars[i]=(x,y,z)
    def draw(self, fb: Framebuffer):
        for x,y,z in self.stars:
            if z<=0: continue
            sx=int(64+x*80/z); sy=int(32+y*40/z)
            if 0<=sx<128 and 0<=sy<64:
                fb.pixel(sx,sy)
                if z<0.3: fb.pixel(sx+1,sy); fb.pixel(sx,sy+1)
