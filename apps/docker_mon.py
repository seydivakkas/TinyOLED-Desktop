"""TinyOLED Desktop — Docker Konteyner Monitörü"""
import subprocess
from core.framebuffer import Framebuffer
from core.font import Font
CONTENT_Y=10; LINE_H=Font.CHAR_H+2

class DockerMonApp:
    NAME="docker"; LABEL="Dockr"; ICON="docker"
    def __init__(self, on_exit, notify=None):
        self.on_exit=on_exit; self.notify=notify; self._cursor=0; self._scroll=0
        self.containers=[]; self.update()
    def on_up(self):
        if self._cursor>0: self._cursor-=1
        if self._cursor<self._scroll: self._scroll=self._cursor
    def on_down(self):
        if self._cursor<len(self.containers)-1: self._cursor+=1
        if self._cursor>=self._scroll+4: self._scroll+=1
    def on_sel(self):
        if not self.containers: return
        c=self.containers[self._cursor]
        cmd="stop" if c["status"]=="running" else "start"
        try: subprocess.run(["docker",cmd,c["id"]],timeout=10,check=True)
        except: pass
        self.update()
    def on_long(self): self.on_exit()
    def update(self):
        try:
            out=subprocess.check_output(["docker","ps","-a","--format","{{.ID}}|{{.Names}}|{{.Status}}"],text=True,stderr=subprocess.DEVNULL)
            self.containers=[]
            for line in out.strip().split("\n"):
                if "|" in line:
                    p=line.split("|"); st="running" if "Up" in p[2] else "stopped"
                    self.containers.append({"id":p[0],"name":p[1][:14],"status":st})
        except: self.containers=[]
    def draw(self, fb: Framebuffer):
        fb.icon("docker",1,CONTENT_Y); fb.text(f"Docker ({len(self.containers)})",12,CONTENT_Y)
        fb.hline(0,CONTENT_Y+9,128); y=CONTENT_Y+11
        if not self.containers:
            fb.text_centered("Konteyner yok",y+10); return
        vis=self.containers[self._scroll:self._scroll+4]
        for i,c in enumerate(vis):
            ai=self._scroll+i; sel=(ai==self._cursor)
            if sel: fb.rect(0,y-1,128,LINE_H+1,fill=True)
            mark=">" if c["status"]=="running" else "x"
            fb.text(f"{mark} {c['name'][:16]}",1,y,on=not sel)
            y+=LINE_H
        fb.text("SEL:toggle",1,56); fb.text("LONG:geri",75,56)
