"""TinyOLED Desktop — Nefes Egzersizi Rehberi"""
import math, time
from core.framebuffer import Framebuffer
PHASES=[("NEFES AL",4.0),("TUT",7.0),("NEFES VER",8.0)]

class BreathingApp:
    NAME="breath"; LABEL="Nefes"; ICON="breath"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.running=False; self.phase=0; self.start=0; self.cycles=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self):
        if not self.running: self.running=True; self.phase=0; self.start=time.monotonic(); self.cycles=0
        else: self.running=False
    def on_long(self): self.on_exit()
    def update(self):
        if not self.running: return
        elapsed=time.monotonic()-self.start
        if elapsed>=PHASES[self.phase][1]:
            self.phase+=1
            if self.phase>=len(PHASES): self.phase=0; self.cycles+=1
            self.start=time.monotonic()
    def draw(self, fb: Framebuffer):
        if not self.running:
            fb.text_centered("Nefes Egzersizi",14); fb.text_centered("4-7-8 Teknigi",26)
            fb.text_centered("[SEL] Basla",42); return
        name,dur=PHASES[self.phase]; elapsed=time.monotonic()-self.start
        prog=min(1,elapsed/dur); rem=max(0,dur-elapsed)
        fb.text_centered(name,10); cx,cy=64,38; mn,mx=4,22
        if self.phase==0: r=int(mn+(mx-mn)*prog)
        elif self.phase==1: r=mx+int(math.sin(elapsed*6)*1.5)
        else: r=int(mx-(mx-mn)*prog)
        fb.circle(cx,cy,r,fill=True); fb.circle(cx,cy,mx+2)
        fb.text(f"{rem:.0f}s",110,34); fb.text(f"Dongu:{self.cycles}",2,56)
