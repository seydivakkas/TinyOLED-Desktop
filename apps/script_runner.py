"""TinyOLED Desktop — Bash Script Runner"""
import subprocess, json, threading
from pathlib import Path
from core.framebuffer import Framebuffer
from core.font import Font
CMD_FILE=Path("/home/pi/tiny-oled-desktop/config/commands.json")
LINE_H=Font.CHAR_H+2

class ScriptRunnerApp:
    NAME="scripts"; LABEL="Komut"; ICON="script"
    def __init__(self, on_exit, notify=None):
        self.on_exit=on_exit; self.notify=notify or (lambda m:None)
        self._cursor=0; self._scroll=0; self._running=False
        self.commands=self._load()
    def _load(self):
        try: return json.loads(CMD_FILE.read_text())
        except: return [{"name":"Uptime","cmd":"uptime"},{"name":"Disk","cmd":"df -h /"},{"name":"Update","cmd":"sudo apt update"}]
    def on_up(self):
        if self._cursor>0: self._cursor-=1
        if self._cursor<self._scroll: self._scroll=self._cursor
    def on_down(self):
        if self._cursor<len(self.commands)-1: self._cursor+=1
        if self._cursor>=self._scroll+4: self._scroll+=1
    def on_sel(self):
        if self._running: return
        cmd=self.commands[self._cursor]
        self._running=True
        def run():
            try:
                subprocess.run(cmd["cmd"],shell=True,timeout=30)
                self.notify(f"OK: {cmd['name'][:12]}")
            except: self.notify(f"HATA: {cmd['name'][:10]}")
            self._running=False
        threading.Thread(target=run,daemon=True).start()
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("script",1,10); fb.text("Komutlar",12,10)
        fb.hline(0,18,128); y=20
        vis=self.commands[self._scroll:self._scroll+4]
        for i,cmd in enumerate(vis):
            ai=self._scroll+i; sel=(ai==self._cursor)
            if sel: fb.rect(0,y-1,128,LINE_H+1,fill=True)
            fb.text(cmd["name"][:20],2,y,on=not sel); y+=LINE_H
        if self._running: fb.text("Calisiyor...",2,56)
        else: fb.text("SEL:calistir",2,56)
