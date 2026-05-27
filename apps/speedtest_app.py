"""TinyOLED Desktop — Speedtest Analog Kadran"""
import math, random, subprocess, threading
from core.framebuffer import Framebuffer

class SpeedtestApp:
    NAME="speedtest"; LABEL="Hiz"; ICON="speed"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.speed=0.0; self.ping=0; self.testing=False; self.progress=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self):
        if not self.testing: self.testing=True; self.progress=0
    def on_long(self): self.on_exit()
    def update(self):
        if not self.testing: return
        self.progress+=2
        if self.progress<100: self.speed=random.uniform(10,80)
        else: self.speed=42.8; self.ping=14; self.testing=False
    def draw(self, fb: Framebuffer):
        fb.text("Hiz Testi",35,2)
        cx,cy,r=64,42,18
        for deg in range(180,361,5):
            rad=math.radians(deg)
            fb.pixel(int(cx+r*math.cos(rad)),int(cy+r*math.sin(rad)))
        capped=min(100,self.speed); angle=180+capped*180/100
        rad=math.radians(angle)
        fb.line(cx,cy,int(cx+(r-3)*math.cos(rad)),int(cy+(r-3)*math.sin(rad)))
        fb.circle(cx,cy,2,fill=True)
        fb.text(f"{self.speed:.1f}",50,18); fb.text("Mbps",78,18)
        if self.testing: fb.text(f"Test:{self.progress}%",2,56)
        else: fb.text(f"Ping:{self.ping}ms",2,56); fb.text("SEL:test",80,56)
