"""TinyOLED Desktop — Bouncing DVD Logo"""
import time
from core.framebuffer import Framebuffer
from core.font import Font

class DVDLogoApp:
    NAME="dvd"; LABEL="DVD"; ICON="dvd"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.x=30.0; self.y=20.0; self.dx=1.5; self.dy=1.0
        self.inverted=False; self._last=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): pass
    def on_long(self): self.on_exit()
    def update(self):
        now=time.monotonic()
        if now-self._last<0.04: return
        self._last=now
        self.x+=self.dx; self.y+=self.dy
        tw=Font.text_width("TinyOLED"); th=7
        if self.x<=0 or self.x+tw>=128:
            self.dx=-self.dx; self.inverted=not self.inverted
        if self.y<=0 or self.y+th>=64:
            self.dy=-self.dy; self.inverted=not self.inverted
        self.x=max(0,min(128-tw,self.x)); self.y=max(0,min(64-th,self.y))
    def draw(self, fb: Framebuffer):
        ix,iy=int(self.x),int(self.y)
        tw=Font.text_width("TinyOLED")
        if self.inverted:
            fb.rect(ix-2,iy-2,tw+4,11,fill=True)
            fb.text("TinyOLED",ix,iy,on=False)
        else:
            fb.text("TinyOLED",ix,iy)
            fb.rect(ix-2,iy-2,tw+4,11)
