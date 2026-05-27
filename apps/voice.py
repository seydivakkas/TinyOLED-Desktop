"""TinyOLED Desktop — Offline Sesli Kontrol"""
import math, time
from core.framebuffer import Framebuffer

class VoiceApp:
    NAME="voice"; LABEL="Ses"; ICON="mic"
    def __init__(self, on_exit, notify=None):
        self.on_exit=on_exit; self.notify=notify or (lambda m:None)
        self.listening=False; self.last_cmd=""; self._phase=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self):
        if not self.listening:
            self.listening=True; self.last_cmd=""
            # Gerçekte: Vosk model yükle + ses dinle
        else: self.listening=False
    def on_long(self): self.on_exit()
    def update(self):
        if self.listening: self._phase+=1
    def draw(self, fb: Framebuffer):
        fb.icon("mic",1,10); fb.text("Ses Kontrol",12,10); fb.hline(0,18,128)
        if self.listening:
            fb.text_centered("Dinliyorum...",28)
            # Ses dalgası animasyonu
            cx=64
            for i in range(20):
                h=int(8*math.sin(self._phase*0.3+i*0.5))
                x=cx-50+i*5; y=44
                fb.line(x,y-abs(h),x,y+abs(h))
        else:
            fb.text_centered("[SEL] Dinle",34)
        if self.last_cmd: fb.text(f"Komut: {self.last_cmd[:16]}",2,56)
