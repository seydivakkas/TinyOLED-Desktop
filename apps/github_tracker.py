"""TinyOLED Desktop — GitHub Tracker"""
from core.framebuffer import Framebuffer
import random

class GitHubTrackerApp:
    NAME="github"; LABEL="Git"; ICON="github"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.user="user"; self.streak=12; self.today=3
        self.grid=[[random.randint(0,3) for _ in range(7)] for _ in range(5)]
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): pass
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("github",1,10); fb.text("GitHub",12,10); fb.hline(0,18,128)
        fb.text(f"Streak: {self.streak} gun",2,22)
        fb.text(f"Bugun : {self.today} commit",2,32)
        gx,gy=78,22
        for r in range(5):
            for c in range(7):
                bx,by=gx+c*7,gy+r*7
                if self.grid[r][c]==0: fb.rect(bx,by,5,5)
                else: fb.rect(bx,by,5,5,fill=True)
