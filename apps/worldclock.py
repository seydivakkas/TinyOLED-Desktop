"""TinyOLED Desktop — Dünya Saati"""
import time
from core.framebuffer import Framebuffer
ZONES=[("Istanbul",3),("London",0),("New York",-5),("Tokyo",9),("Sydney",10)]

class WorldClockApp:
    NAME="worldclock"; LABEL="Dunya"; ICON="world"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._cursor=0
    def on_up(self): self._cursor=max(0,self._cursor-1)
    def on_down(self): self._cursor=min(len(ZONES)-1,self._cursor+1)
    def on_sel(self): pass
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("world",1,10); fb.text("Dunya Saati",12,10); fb.hline(0,18,128); y=21
        utc=time.time()
        for i,(name,off) in enumerate(ZONES):
            sel=(i==self._cursor); lt=time.gmtime(utc+off*3600)
            ts=f"{lt.tm_hour:02d}:{lt.tm_min:02d}"
            if sel: fb.rect(0,y-1,128,9,fill=True)
            fb.text(f"{name[:8]:8s} {ts}",2,y,on=not sel); y+=9
