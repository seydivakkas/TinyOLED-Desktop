"""TinyOLED Desktop — Pi-hole Dashboard"""
import json
from core.framebuffer import Framebuffer

class PiholeApp:
    NAME="pihole"; LABEL="Pi-h"; ICON="pihole"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.blocked=0; self.total=0; self.pct=0; self.enabled=True
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self):
        try:
            import urllib.request
            if self.enabled: urllib.request.urlopen("http://localhost/admin/api.php?disable=30",timeout=3)
            else: urllib.request.urlopen("http://localhost/admin/api.php?enable",timeout=3)
            self.enabled=not self.enabled
        except: pass
    def on_long(self): self.on_exit()
    def update(self):
        try:
            import urllib.request
            r=urllib.request.urlopen("http://localhost/admin/api.php?summary",timeout=3)
            d=json.loads(r.read())
            self.blocked=int(d.get("ads_blocked_today",0))
            self.total=int(d.get("dns_queries_today",0))
            self.pct=float(d.get("ads_percentage_today",0))
        except: pass
    def draw(self, fb: Framebuffer):
        fb.icon("pihole",1,10); fb.text("Pi-hole",12,10); fb.hline(0,18,128)
        fb.text(f"Engellenen: {self.blocked}",2,24)
        fb.text(f"Toplam    : {self.total}",2,34)
        fb.progress_bar(2,44,124,6,self.pct)
        fb.text(f"%{self.pct:.1f}",50,52)
        fb.text("ON" if self.enabled else "OFF",100,52)
