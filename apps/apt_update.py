"""TinyOLED Desktop — APT Güncelleme Bildirici"""
import subprocess, threading
from core.framebuffer import Framebuffer

class APTUpdateApp:
    NAME="apt"; LABEL="APT"; ICON="apt"
    def __init__(self, on_exit, notify=None):
        self.on_exit=on_exit; self.notify=notify or (lambda m:None)
        self.count=0; self.checking=False; self.packages=[]; self._check()
    def _check(self):
        self.checking=True
        def do():
            try:
                out=subprocess.check_output(["apt","list","--upgradable"],text=True,stderr=subprocess.DEVNULL)
                self.packages=[l.split("/")[0] for l in out.strip().split("\n")[1:] if "/" in l]
                self.count=len(self.packages)
            except: self.count=0; self.packages=[]
            self.checking=False
        threading.Thread(target=do,daemon=True).start()
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self._check()
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("apt",1,10); fb.text("APT Guncelleme",12,10); fb.hline(0,18,128)
        if self.checking: fb.text_centered("Kontrol ediliyor...",30); return
        fb.text_centered(f"{self.count} guncelleme mevcut",24)
        y=34
        for pkg in self.packages[:3]:
            fb.text(f"- {pkg[:20]}",5,y); y+=9
        if self.count>3: fb.text(f"  +{self.count-3} daha...",5,y)
        fb.text("SEL:kontrol",2,56)
