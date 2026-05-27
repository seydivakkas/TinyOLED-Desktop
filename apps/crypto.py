"""TinyOLED Desktop — Kripto Para Takipçisi"""
import time, json
from core.framebuffer import Framebuffer

class CryptoApp:
    NAME="crypto"; LABEL="Kripto"; ICON="crypto"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._cursor=0; self._last=0
        self.coins=[
            {"name":"BTC","price":67420.50,"change":2.4},
            {"name":"ETH","price":3521.80,"change":-1.2},
            {"name":"SOL","price":142.35,"change":5.8},
        ]
    def on_up(self): self._cursor=max(0,self._cursor-1)
    def on_down(self): self._cursor=min(len(self.coins)-1,self._cursor+1)
    def on_sel(self): self._fetch()
    def on_long(self): self.on_exit()
    def _fetch(self):
        try:
            import urllib.request
            r=urllib.request.urlopen("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true",timeout=5)
            d=json.loads(r.read())
            self.coins=[
                {"name":"BTC","price":d["bitcoin"]["usd"],"change":d["bitcoin"].get("usd_24h_change",0)},
                {"name":"ETH","price":d["ethereum"]["usd"],"change":d["ethereum"].get("usd_24h_change",0)},
                {"name":"SOL","price":d["solana"]["usd"],"change":d["solana"].get("usd_24h_change",0)},
            ]
        except: pass
    def update(self):
        now=time.monotonic()
        if now-self._last<300: return
        self._last=now; self._fetch()
    def draw(self, fb: Framebuffer):
        fb.icon("crypto",1,10); fb.text("Kripto Fiyatlar",12,10)
        fb.hline(0,18,128); y=22
        for i,c in enumerate(self.coins):
            sel=(i==self._cursor)
            if sel: fb.rect(0,y-1,128,12,fill=True)
            arrow="^" if c["change"]>=0 else "v"
            fb.text(f"{c['name']} ${c['price']:.0f} {arrow}{abs(c['change']):.1f}%",2,y,on=not sel)
            y+=13
        fb.text("SEL:guncelle",2,56)
