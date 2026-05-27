"""TinyOLED Desktop — Pomodoro Zamanlayıcı"""
import time
from core.framebuffer import Framebuffer

class PomodoroApp:
    NAME="pomodoro"; LABEL="Pomo"; ICON="timer"
    WORK=25*60; BREAK=5*60
    def __init__(self, on_exit, notify=None):
        self.on_exit=on_exit; self.notify=notify or (lambda m:None)
        self.running=False; self.working=True; self.remaining=self.WORK; self.sessions=0; self._last=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self):
        if not self.running: self.running=True; self._last=time.monotonic()
        else: self.running=False
    def on_long(self): self.on_exit()
    def update(self):
        if not self.running: return
        now=time.monotonic(); dt=now-self._last; self._last=now; self.remaining-=dt
        if self.remaining<=0:
            if self.working: self.sessions+=1; self.notify(f"Mola! ({self.sessions})"); self.remaining=self.BREAK
            else: self.notify("Calismaya basla!"); self.remaining=self.WORK
            self.working=not self.working
    def draw(self, fb: Framebuffer):
        fb.icon("timer",1,10); fb.text("Pomodoro",12,10); fb.hline(0,18,128)
        mins=int(self.remaining)//60; secs=int(self.remaining)%60
        fb.text_centered(f"{mins:02d}:{secs:02d}",30)
        total=self.WORK if self.working else self.BREAK
        fb.progress_bar(10,42,108,6,total-self.remaining,max_val=total)
        fb.text("CALISMA" if self.working else "MOLA",2,52)
        fb.text(f"#{self.sessions}",60,52)
        fb.text("DUR" if self.running else "BASLA",90,52)
