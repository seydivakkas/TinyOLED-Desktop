"""TinyOLED Desktop — Görev Listesi (Todo)"""
import json
from pathlib import Path
from core.framebuffer import Framebuffer
from core.font import Font
SAVE=Path("/home/pi/tiny-oled-desktop/config/todo.json")
LINE_H=Font.CHAR_H+2

class TodoApp:
    NAME="todo"; LABEL="Gorev"; ICON="todo"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._cursor=0; self._scroll=0
        self.tasks=self._load()
    def _load(self):
        try: return json.loads(SAVE.read_text())
        except: return [{"text":"Ornek gorev","done":False},{"text":"Diger gorev","done":True}]
    def _save(self):
        try: SAVE.write_text(json.dumps(self.tasks,indent=2))
        except: pass
    def on_up(self):
        if self._cursor>0: self._cursor-=1
        if self._cursor<self._scroll: self._scroll=self._cursor
    def on_down(self):
        if self._cursor<len(self.tasks)-1: self._cursor+=1
        if self._cursor>=self._scroll+5: self._scroll+=1
    def on_sel(self):
        if not self.tasks: return
        self.tasks[self._cursor]["done"]=not self.tasks[self._cursor]["done"]
        self._save()
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("todo",1,10); fb.text("Gorevler",12,10); fb.hline(0,18,128); y=20
        vis=self.tasks[self._scroll:self._scroll+5]
        for i,t in enumerate(vis):
            ai=self._scroll+i; sel=(ai==self._cursor)
            if sel: fb.rect(0,y-1,128,LINE_H+1,fill=True)
            mark="[x]" if t["done"] else "[ ]"
            fb.text(f"{mark} {t['text'][:16]}",1,y,on=not sel); y+=LINE_H
        done=sum(1 for t in self.tasks if t["done"])
        fb.text(f"{done}/{len(self.tasks)} tamamlandi",2,56)
