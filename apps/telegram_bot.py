"""TinyOLED Desktop — Telegram Bot Bildirim Merkezi"""
from core.framebuffer import Framebuffer
from core.font import Font
LINE_H=Font.CHAR_H+2

class TelegramBotApp:
    NAME="telegram"; LABEL="Telgm"; ICON="telegram"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._cursor=0; self._scroll=0
        self.messages=[{"from":"Bot","text":"TinyOLED hazir!"}]
    def on_up(self):
        if self._cursor>0: self._cursor-=1
        if self._cursor<self._scroll: self._scroll=self._cursor
    def on_down(self):
        if self._cursor<len(self.messages)-1: self._cursor+=1
        if self._cursor>=self._scroll+4: self._scroll+=1
    def on_sel(self): pass  # Hazır yanıt gönder
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("telegram",1,10); fb.text(f"Telegram ({len(self.messages)})",12,10)
        fb.hline(0,18,128); y=20
        vis=self.messages[self._scroll:self._scroll+4]
        for i,m in enumerate(vis):
            ai=self._scroll+i; sel=(ai==self._cursor)
            if sel: fb.rect(0,y-1,128,LINE_H+1,fill=True)
            fb.text(f"{m['from'][:5]}:{m['text'][:14]}",1,y,on=not sel); y+=LINE_H
        fb.text("SEL:yanit",2,56)
