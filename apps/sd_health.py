"""TinyOLED Desktop — SD Kart Sağlık Monitörü"""
import subprocess
from pathlib import Path
from core.framebuffer import Framebuffer

class SDHealthApp:
    NAME="sdhealth"; LABEL="SD"; ICON="sd"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.total="?"; self.used="?"; self.free="?"; self.pct=0; self.update()
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self.update()
    def on_long(self): self.on_exit()
    def update(self):
        try:
            out=subprocess.check_output(["df","-h","/"],text=True,stderr=subprocess.DEVNULL)
            parts=out.strip().split("\n")[1].split()
            self.total=parts[1]; self.used=parts[2]; self.free=parts[3]; self.pct=int(parts[4].replace("%",""))
        except: pass
    def draw(self, fb: Framebuffer):
        fb.icon("sd",1,10); fb.text("SD Kart Sagligi",12,10); fb.hline(0,18,128)
        fb.text(f"Toplam : {self.total}",5,24)
        fb.text(f"Kullan : {self.used}",5,34)
        fb.text(f"Bos    : {self.free}",5,44)
        fb.progress_bar(5,54,90,6,self.pct)
        fb.text(f"%{self.pct}",100,54)
        if self.pct>90: fb.text("!",120,54)
