"""TinyOLED Desktop — DHT Sıcaklık & Nem Sensörü"""
import time, random
from core.framebuffer import Framebuffer

class SensorsApp:
    NAME="sensors"; LABEL="Sensr"; ICON="temp"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.temp=24.5; self.hum=48.0; self._last=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self._read()
    def on_long(self): self.on_exit()
    def _read(self):
        try:
            import Adafruit_DHT
            h,t=Adafruit_DHT.read_retry(11,4)
            if t: self.temp=t
            if h: self.hum=h
        except: self.temp+=random.uniform(-0.2,0.2); self.hum+=random.uniform(-0.5,0.5)
    def update(self):
        now=time.monotonic()
        if now-self._last<3: return
        self._last=now; self._read()
    def draw(self, fb: Framebuffer):
        fb.icon("temp",1,10); fb.text("Oda Istasyonu",12,10); fb.hline(0,18,128)
        fb.text(f"Sicaklik: {self.temp:.1f}C",5,24)
        fb.progress_bar(5,34,118,6,self.temp,max_val=50)
        fb.text(f"Nem     : {self.hum:.1f}%",5,44)
        fb.progress_bar(5,54,118,6,self.hum,max_val=100)
        if self.temp>28: fb.text("!SICAK!",90,24)
