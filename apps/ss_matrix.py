"""TinyOLED Desktop — Matrix Digital Rain"""
import random, time
from core.framebuffer import Framebuffer

COLS=21; ROWS=8

class MatrixRainApp:
    NAME="matrix"; LABEL="Matrx"; ICON="matrix"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._last=0
        self.drops=[random.randint(-ROWS,0) for _ in range(COLS)]
        self.chars=[[random.randint(33,126) for _ in range(ROWS)] for _ in range(COLS)]
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): pass
    def on_long(self): self.on_exit()
    def update(self):
        now=time.monotonic()
        if now-self._last<0.1: return
        self._last=now
        for c in range(COLS):
            self.drops[c]+=1
            if self.drops[c]>ROWS+4: self.drops[c]=random.randint(-4,0)
            self.chars[c][self.drops[c]%ROWS]=random.randint(33,126)
    def draw(self, fb: Framebuffer):
        for c in range(COLS):
            x=c*6+1
            drop_y=self.drops[c]
            for r in range(ROWS):
                if r<=drop_y and r>drop_y-5:
                    ch=chr(self.chars[c][r%ROWS])
                    y=r*8
                    if r==drop_y:
                        fb.rect(x-1,y-1,7,9,fill=True)
                        fb.text(ch,x,y,on=False)
                    else:
                        fb.text(ch,x,y)
