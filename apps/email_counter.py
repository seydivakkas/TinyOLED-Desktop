"""TinyOLED Desktop — Email Okunmamış Sayacı"""
from core.framebuffer import Framebuffer

class EmailCounterApp:
    NAME="email"; LABEL="Email"; ICON="email"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.unread=0; self._last=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self._check()
    def on_long(self): self.on_exit()
    def _check(self):
        try:
            import imaplib; m=imaplib.IMAP4_SSL("imap.gmail.com")
            m.login("user","pass"); m.select("inbox")
            _,data=m.search(None,"UNSEEN"); self.unread=len(data[0].split()); m.logout()
        except: pass
    def update(self):
        import time; now=time.monotonic()
        if now-self._last<60: return
        self._last=now; self._check()
    def draw(self, fb: Framebuffer):
        fb.icon("email",1,10); fb.text("E-posta",12,10); fb.hline(0,18,128)
        # Büyük sayı
        s=str(self.unread)
        from core.font import Font
        scale=4; tw=len(s)*6*scale; sx=(128-tw)//2
        for ch in s:
            cols=Font.glyph(ch)
            for ci,col in enumerate(cols):
                for ri in range(7):
                    if col&(1<<ri): fb.rect(sx+ci*scale,26+ri*scale,scale,scale,fill=True)
            sx+=6*scale
        fb.text_centered("okunmamis e-posta",56)
