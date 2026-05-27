"""TinyOLED Desktop — Pixel Art Editörü"""
from core.framebuffer import Framebuffer

class PixelArtApp:
    NAME="pixelart"; LABEL="Pixel"; ICON="paint"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.cx=64; self.cy=32; self.drawing=False
        self.canvas=set()
    def on_up(self):
        if self.drawing: self.cy=max(0,self.cy-1); self.canvas.add((self.cx,self.cy))
        else: self.cy=max(0,self.cy-1)
    def on_down(self):
        if self.drawing: self.cy=min(63,self.cy+1); self.canvas.add((self.cx,self.cy))
        else: self.cy=min(63,self.cy+1)
    def on_sel(self):
        if self.drawing: self.cx=min(127,self.cx+1); self.canvas.add((self.cx,self.cy))
        else: self.drawing=not self.drawing
    def on_long(self):
        if self.drawing: self.drawing=False
        else: self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        for x,y in self.canvas: fb.pixel(x,y)
        # İmleç
        if int(__import__("time").monotonic()*4)%2:
            fb.pixel(self.cx,self.cy)
            fb.pixel(self.cx-1,self.cy); fb.pixel(self.cx+1,self.cy)
            fb.pixel(self.cx,self.cy-1); fb.pixel(self.cx,self.cy+1)
        fb.text("D" if self.drawing else "M",0,0)
