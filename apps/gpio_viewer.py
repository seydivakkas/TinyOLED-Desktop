"""TinyOLED Desktop — GPIO Pin Viewer"""
import subprocess
from core.framebuffer import Framebuffer
GPIO_PINS=[2,3,4,17,27,22,10,9,11,0,5,6,13,19,26,14,15,18,23,24,25,8,7,1,12,16,20,21]

class GPIOViewerApp:
    NAME="gpio"; LABEL="GPIO"; ICON="pin"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._cursor=0; self._scroll=0
        self.states={}; self.update()
    def _read_pin(self, pin):
        try:
            v=subprocess.check_output(["cat",f"/sys/class/gpio/gpio{pin}/value"],text=True,stderr=subprocess.DEVNULL).strip()
            return int(v)
        except: return -1
    def on_up(self):
        if self._cursor>0: self._cursor-=1
        if self._cursor<self._scroll: self._scroll=self._cursor
    def on_down(self):
        if self._cursor<len(GPIO_PINS)-1: self._cursor+=1
        if self._cursor>=self._scroll+5: self._scroll+=1
    def on_sel(self):
        pin=GPIO_PINS[self._cursor]
        try:
            cur=self.states.get(pin,0); nv=0 if cur==1 else 1
            subprocess.run(["bash","-c",f"echo {nv} > /sys/class/gpio/gpio{pin}/value"],timeout=2)
        except: pass
        self.update()
    def on_long(self): self.on_exit()
    def update(self):
        for p in GPIO_PINS: self.states[p]=self._read_pin(p)
    def draw(self, fb: Framebuffer):
        fb.icon("pin",1,10); fb.text("GPIO Pinleri",12,10)
        fb.hline(0,18,128); y=20
        vis=GPIO_PINS[self._scroll:self._scroll+5]
        for i,pin in enumerate(vis):
            ai=self._scroll+i; sel=(ai==self._cursor)
            if sel: fb.rect(0,y-1,128,8,fill=True)
            v=self.states.get(pin,-1)
            st="H" if v==1 else ("L" if v==0 else "?")
            fb.text(f"GPIO{pin:2d}: {st}",2,y,on=not sel)
            bx=90; bw=30
            if v==1: fb.rect(bx,y,bw,6,fill=True,on=not sel)
            else: fb.rect(bx,y,bw,6,on=not sel)
            y+=8
        fb.text("SEL:toggle",1,56)
