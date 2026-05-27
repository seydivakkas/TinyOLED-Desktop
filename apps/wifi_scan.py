"""TinyOLED Desktop — WiFi Ağ Tarayıcı"""
import subprocess, threading
from core.framebuffer import Framebuffer
from core.font import Font
LINE_H=Font.CHAR_H+2

class WiFiScanApp:
    NAME="wifiscan"; LABEL="Tara"; ICON="radar"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._cursor=0; self._scroll=0
        self.networks=[]; self._scanning=False; self.scan()
    def scan(self):
        self._scanning=True
        def do():
            try:
                out=subprocess.check_output(["sudo","iwlist","wlan0","scan"],text=True,stderr=subprocess.DEVNULL)
                self.networks=[]
                for block in out.split("Cell ")[1:]:
                    ssid=ch=sig=enc=""
                    for l in block.split("\n"):
                        l=l.strip()
                        if "ESSID:" in l: ssid=l.split('"')[1] if '"' in l else ""
                        elif "Channel:" in l: ch=l.split(":")[1]
                        elif "Signal level=" in l:
                            try: sig=l.split("Signal level=")[1].split()[0]
                            except: sig="?"
                        elif "Encryption key:" in l: enc="WPA" if "on" in l else "Open"
                    if ssid: self.networks.append({"ssid":ssid,"ch":ch,"sig":sig,"enc":enc})
            except: self.networks=[]
            self._scanning=False
        threading.Thread(target=do,daemon=True).start()
    def on_up(self):
        if self._cursor>0: self._cursor-=1
        if self._cursor<self._scroll: self._scroll=self._cursor
    def on_down(self):
        if self._cursor<len(self.networks)-1: self._cursor+=1
        if self._cursor>=self._scroll+4: self._scroll+=1
    def on_sel(self): self.scan()
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("radar",1,10)
        fb.text("Taranıyor..." if self._scanning else f"WiFi ({len(self.networks)})",12,10)
        fb.hline(0,18,128); y=20
        vis=self.networks[self._scroll:self._scroll+4]
        for i,n in enumerate(vis):
            ai=self._scroll+i; sel=(ai==self._cursor)
            if sel: fb.rect(0,y-1,128,LINE_H+1,fill=True)
            fb.text(f"{n['ssid'][:12]} Ch{n['ch']} {n['enc'][:3]}",1,y,on=not sel)
            y+=LINE_H
        fb.text("SEL:tara",2,56)
