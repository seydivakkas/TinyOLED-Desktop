"""TinyOLED Desktop — Conway's Game of Life"""
import random, time
from core.framebuffer import Framebuffer

W,H=128,64

class GameOfLifeApp:
    NAME="life"; LABEL="Life"; ICON="cell"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._last=0; self.gen=0; self.randomize()
    def randomize(self):
        self.grid=[[random.random()<0.3 for _ in range(W)] for _ in range(H)]
        self.gen=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self.randomize()
    def on_long(self): self.on_exit()
    def _neighbors(self, x, y):
        c=0
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                nx,ny=(x+dx)%W,(y+dy)%H
                if self.grid[ny][nx]: c+=1
        return c
    def update(self):
        now=time.monotonic()
        if now-self._last<0.15: return
        self._last=now; self.gen+=1
        new=[[False]*W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                n=self._neighbors(x,y)
                if self.grid[y][x]: new[y][x]=(n==2 or n==3)
                else: new[y][x]=(n==3)
        self.grid=new
    def draw(self, fb: Framebuffer):
        for y in range(H):
            for x in range(W):
                if self.grid[y][x]: fb.pixel(x,y)
