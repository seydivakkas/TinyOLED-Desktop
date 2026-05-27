"""TinyOLED Desktop — Mandelbrot Fraktal Gezgini"""
from core.framebuffer import Framebuffer

class FractalApp:
    NAME="fractal"; LABEL="Fraktl"; ICON="fractal"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.cx=-0.5; self.cy=0.0; self.zoom=1.5; self.max_iter=20
    def on_up(self): self.zoom*=0.7; self.max_iter=min(50,self.max_iter+2)
    def on_down(self): self.zoom*=1.4; self.max_iter=max(10,self.max_iter-2)
    def on_sel(self): self.cx=-0.5; self.cy=0.0; self.zoom=1.5; self.max_iter=20
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        for py in range(64):
            for px in range(128):
                x0=self.cx+(px-64)*self.zoom/64
                y0=self.cy+(py-32)*self.zoom/32
                x,y,i=0.0,0.0,0
                while x*x+y*y<=4 and i<self.max_iter:
                    x,y=x*x-y*y+x0,2*x*y+y0; i+=1
                if i<self.max_iter: fb.pixel(px,py)
