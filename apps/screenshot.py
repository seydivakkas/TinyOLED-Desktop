"""TinyOLED Desktop — Ekran Görüntüsü"""
import time
from pathlib import Path
from core.framebuffer import Framebuffer

class ScreenshotApp:
    NAME="screenshot"; LABEL="SS"; ICON="camera"
    def __init__(self, on_exit, notify=None):
        self.on_exit=on_exit; self.notify=notify or (lambda m:None)
        self.count=0; self.last_file=""
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self._capture()
    def on_long(self): self.on_exit()
    def _capture(self):
        self.count+=1; ts=int(time.time())
        self.last_file=f"/tmp/oled_cap_{ts}.pbm"
        self.notify(f"Kaydedildi: #{self.count}")
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("camera",1,10); fb.text("Ekran Goruntusu",12,10); fb.hline(0,18,128)
        fb.text_centered(f"Toplam: {self.count} kayit",28)
        if self.last_file: fb.text(self.last_file[-20:],4,40)
        fb.text_centered("[SEL] Yakala",54)
