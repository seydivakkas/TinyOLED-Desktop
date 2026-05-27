"""TinyOLED Desktop — HackerNews QR Okuyucu"""
from core.framebuffer import Framebuffer
from core.font import Font
LINE_H=Font.CHAR_H+2

class HackerNewsApp:
    NAME="hackernews"; LABEL="HN"; ICON="news"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._cursor=0; self._scroll=0; self.qr_mode=False
        self.stories=[
            {"title":"Raspberry Pi Zero artik cok iyi","url":"https://rpi.com"},
            {"title":"SSD1306 OLED hakkinda bilgiler","url":"https://wiki.org"},
            {"title":"Python ile 3D motor yazmak","url":"https://github.com"},
            {"title":"Show HN: TinyOLED Desktop OS","url":"https://news.yc.com"},
            {"title":"Monokrom arayuz tasarimi","url":"https://medium.com"},
        ]
    def on_up(self):
        if self.qr_mode: self.qr_mode=False; return
        if self._cursor>0: self._cursor-=1
        if self._cursor<self._scroll: self._scroll=self._cursor
    def on_down(self):
        if self.qr_mode: self.qr_mode=False; return
        if self._cursor<len(self.stories)-1: self._cursor+=1
        if self._cursor>=self._scroll+4: self._scroll+=1
    def on_sel(self): self.qr_mode=not self.qr_mode
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        if self.qr_mode:
            fb.text("QR ile Oku",30,2); fb.hline(0,10,128)
            for r in range(21):
                for c in range(21):
                    if ((r+c)%3==0) or (r<7 and c<7) or (r<7 and c>13) or (r>13 and c<7):
                        fb.rect(4+c*2,14+r*2,2,2,fill=True)
            fb.text("Tarat ve",50,20); fb.text("haberi oku",50,32)
            return
        fb.icon("news",1,10); fb.text("HackerNews",12,10)
        fb.hline(0,18,128); y=20
        vis=self.stories[self._scroll:self._scroll+4]
        for i,s in enumerate(vis):
            ai=self._scroll+i; sel=(ai==self._cursor)
            if sel: fb.rect(0,y-1,128,LINE_H+1,fill=True)
            fb.text(s["title"][:21],2,y,on=not sel); y+=LINE_H
        fb.text("SEL:QR",2,56)
