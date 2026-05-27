"""TinyOLED Desktop — Systemd Servis Yöneticisi"""
import subprocess
from core.framebuffer import Framebuffer
from core.font import Font
CONTENT_Y=10; LINE_H=Font.CHAR_H+2
SERVICES=["ssh","nginx","docker","pihole-FTL","cron","bluetooth"]

class SystemdMonApp:
    NAME="systemd"; LABEL="Servi"; ICON="service"
    def __init__(self, on_exit, notify=None):
        self.on_exit=on_exit; self.notify=notify; self._cursor=0; self._scroll=0
        self.states={}; self.update()
    def _check(self, svc):
        try:
            r=subprocess.run(["systemctl","is-active",svc],capture_output=True,text=True,timeout=3)
            return r.stdout.strip()=="active"
        except: return False
    def on_up(self):
        if self._cursor>0: self._cursor-=1
        if self._cursor<self._scroll: self._scroll=self._cursor
    def on_down(self):
        if self._cursor<len(SERVICES)-1: self._cursor+=1
        if self._cursor>=self._scroll+4: self._scroll+=1
    def on_sel(self):
        svc=SERVICES[self._cursor]
        try: subprocess.run(["sudo","systemctl","restart",svc],timeout=10)
        except: pass
        self.update()
    def on_long(self): self.on_exit()
    def update(self):
        for s in SERVICES: self.states[s]=self._check(s)
    def draw(self, fb: Framebuffer):
        fb.icon("service",1,CONTENT_Y); fb.text("Servisler",12,CONTENT_Y)
        fb.hline(0,CONTENT_Y+9,128); y=CONTENT_Y+11
        vis=SERVICES[self._scroll:self._scroll+4]
        for i,svc in enumerate(vis):
            ai=self._scroll+i; sel=(ai==self._cursor)
            if sel: fb.rect(0,y-1,128,LINE_H+1,fill=True)
            active=self.states.get(svc,False)
            mark="+" if active else "-"
            fb.text(f"{mark} {svc[:16]}",1,y,on=not sel)
            y+=LINE_H
        fb.text("SEL:restart",1,56); fb.text("LONG:geri",75,56)
