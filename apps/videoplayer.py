"""TinyOLED Desktop — Bad Apple 1-bit Video Player"""
import time
from core.framebuffer import Framebuffer

class VideoPlayerApp:
    NAME="video"; LABEL="Video"; ICON="video"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.playing=False; self.frame=0; self.total=600; self._last=0
    def on_up(self): self.playing=not self.playing
    def on_down(self): self.frame=0
    def on_sel(self):
        if not self.playing: self.playing=True
        else: self.playing=False
    def on_long(self): self.on_exit()
    def update(self):
        if not self.playing: return
        now=time.monotonic()
        if now-self._last<0.05: return
        self._last=now; self.frame+=1
        if self.frame>=self.total: self.frame=0; self.playing=False
    def draw(self, fb: Framebuffer):
        if not self.playing and self.frame==0:
            fb.text_centered("Bad Apple!! Video",20)
            fb.text_centered("[SEL] Oynat",35); fb.text_centered("[DOWN] Basa Sar",48)
            return
        # Animasyon simülasyonu — gerçekte binary dosyadan okunur
        import math
        t=self.frame*0.1
        cx,cy=64+int(20*math.sin(t)),32+int(10*math.cos(t*0.7))
        r=int(15+10*math.sin(t*0.5))
        fb.circle(cx,cy,r,fill=True)
        fb.circle(cx-30,cy+5,r//2,fill=True)
        fb.progress_bar(10,58,108,4,self.frame,max_val=self.total)
