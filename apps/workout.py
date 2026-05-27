"""TinyOLED Desktop — HIIT/Tabata Egzersiz Zamanlayıcı"""
import time
from core.framebuffer import Framebuffer
PRESETS=[("Tabata",20,10,8),("HIIT 30/15",30,15,6),("Custom",40,20,4)]

class WorkoutApp:
    NAME="workout"; LABEL="HIIT"; ICON="workout"
    def __init__(self, on_exit, notify=None):
        self.on_exit=on_exit; self.notify=notify or (lambda m:None)
        self._preset=0; self.running=False; self.work=True; self.remaining=0
        self.round=0; self.total_rounds=0; self._last=0
    def on_up(self): self._preset=(self._preset-1)%len(PRESETS)
    def on_down(self): self._preset=(self._preset+1)%len(PRESETS)
    def on_sel(self):
        if not self.running:
            _,w,_,r=PRESETS[self._preset]; self.running=True; self.work=True
            self.remaining=w; self.round=1; self.total_rounds=r; self._last=time.monotonic()
        else: self.running=False
    def on_long(self): self.on_exit()
    def update(self):
        if not self.running: return
        now=time.monotonic(); self.remaining-=now-self._last; self._last=now
        if self.remaining<=0:
            _,w,b,_=PRESETS[self._preset]
            if self.work: self.remaining=b; self.work=False; self.notify("MOLA!")
            else:
                self.round+=1
                if self.round>self.total_rounds: self.running=False; self.notify("BITTI!"); return
                self.remaining=w; self.work=True; self.notify(f"Round {self.round}!")
    def draw(self, fb: Framebuffer):
        if not self.running:
            fb.text_centered("Egzersiz Timer",14)
            for i,(name,w,b,r) in enumerate(PRESETS):
                sel=(i==self._preset)
                if sel: fb.rect(0,24+i*10,128,10,fill=True)
                fb.text(f"{name} {w}s/{b}s x{r}",2,25+i*10,on=not sel)
            fb.text_centered("[SEL] Basla",56); return
        s=max(0,int(self.remaining)); phase="CALIS" if self.work else "DINLEN"
        if self.work: fb.rect(0,0,128,64,fill=True); on=False
        else: on=True
        fb.text_centered(phase,10,on=on); fb.text_centered(f"{s}",28,on=on)
        fb.text(f"R:{self.round}/{self.total_rounds}",2,55,on=on)
