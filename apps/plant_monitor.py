"""TinyOLED Desktop — Bitki Sulama Monitörü"""
import time, random
from core.framebuffer import Framebuffer

class PlantMonitorApp:
    NAME="plant"; LABEL="Bitki"; ICON="plant"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.moisture=65; self.watering=False; self._last=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self):
        self.watering=True; self.moisture=min(100,self.moisture+30)
    def on_long(self): self.on_exit()
    def _read(self):
        try:
            import spidev; spi=spidev.SpiDev(); spi.open(0,0)
            r=spi.xfer2([1,(0<<4)|0x80,0]); self.moisture=int(((r[1]&3)<<8)+r[2])*100//1023
            spi.close()
        except: self.moisture=max(0,self.moisture-random.randint(0,2))
    def update(self):
        now=time.monotonic()
        if now-self._last<5: return
        self._last=now; self._read(); self.watering=False
    def draw(self, fb: Framebuffer):
        fb.icon("plant",1,10); fb.text("Bitki Bakim",12,10); fb.hline(0,18,128)
        fb.text(f"Toprak Nem: %{self.moisture}",5,24)
        fb.progress_bar(5,34,118,8,self.moisture)
        if self.moisture<30:
            fb.text_centered("!! SUSUZ - SULA !!",46)
        elif self.watering:
            fb.text_centered("SULANIYOR...",46)
        else:
            fb.text_centered("Bitki iyi durumda",46)
        fb.text("SEL:sula",2,56)
