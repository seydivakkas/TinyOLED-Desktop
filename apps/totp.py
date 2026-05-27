"""TinyOLED Desktop — TOTP 2FA Authenticator"""
import hashlib, hmac, struct, time
from core.framebuffer import Framebuffer
from core.font import Font

class TOTPApp:
    NAME="totp"; LABEL="2FA"; ICON="key"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._cursor=0
        self.accounts=[
            {"name":"GitHub","secret":b"JBSWY3DPEHPK3PXP"},
            {"name":"Google","secret":b"HXDMVJECJJWSRB3H"},
            {"name":"Discord","secret":b"GEZDGNBVGY3TQOJQ"},
        ]
    def on_up(self): self._cursor=max(0,self._cursor-1)
    def on_down(self): self._cursor=min(len(self.accounts)-1,self._cursor+1)
    def on_sel(self): pass
    def on_long(self): self.on_exit()
    def _totp(self, secret, period=30):
        counter=int(time.time())//period
        msg=struct.pack(">Q",counter)
        h=hmac.new(secret,msg,hashlib.sha1).digest()
        o=h[-1]&0x0F; code=struct.unpack(">I",h[o:o+4])[0]
        return f"{(code&0x7FFFFFFF)%1000000:06d}"
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("key",1,10); fb.text("2FA Dogrulayici",12,10)
        remaining=30-(int(time.time())%30)
        fb.progress_bar(90,10,36,6,remaining,max_val=30)
        fb.hline(0,18,128); y=21
        for i,a in enumerate(self.accounts):
            sel=(i==self._cursor)
            if sel: fb.rect(0,y-1,128,17,fill=True)
            fb.text(a["name"],2,y,on=not sel)
            code=self._totp(a["secret"])
            fb.text(f"{code[:3]} {code[3:]}",60,y+1,on=not sel)
            y+=18
