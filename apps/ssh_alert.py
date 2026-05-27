"""TinyOLED Desktop — SSH Yetkisiz Giriş Dedektörü"""
import threading, time
from pathlib import Path
from core.framebuffer import Framebuffer

class SSHAlertApp:
    NAME="sshalert"; LABEL="SSH"; ICON="shield"
    def __init__(self, on_exit, notify=None):
        self.on_exit=on_exit; self.notify=notify or (lambda m:None)
        self.attempts=[]; self._last_pos=0; self._running=True
        self._thread=threading.Thread(target=self._watch,daemon=True); self._thread.start()
    def _watch(self):
        while self._running:
            try:
                text=Path("/var/log/auth.log").read_text()
                lines=text[self._last_pos:].split("\n"); self._last_pos=len(text)
                for l in lines:
                    if "Failed password" in l or "Invalid user" in l:
                        parts=l.split(); ip="?"
                        for i,p in enumerate(parts):
                            if p=="from" and i+1<len(parts): ip=parts[i+1]; break
                        self.attempts.append({"time":parts[0]+" "+parts[1]+" "+parts[2],"ip":ip})
                        if len(self.attempts)>20: self.attempts.pop(0)
                        self.notify(f"SSH alert: {ip}")
            except: pass
            time.sleep(5)
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self.attempts.clear()
    def on_long(self): self._running=False; self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("shield",1,10); fb.text(f"SSH ({len(self.attempts)})",12,10)
        fb.hline(0,18,128); y=20
        if not self.attempts:
            fb.text_centered("Temiz - alert yok",30); return
        for a in self.attempts[-4:]:
            fb.text(f"{a['ip'][:15]}",2,y); y+=9
        fb.text("SEL:temizle",2,56)
