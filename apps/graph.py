"""
TinyOLED Desktop — Gerçek Zamanlı CPU/RAM/Sıcaklık Grafiği
UP/DOWN: Metrik değiştir, SEL: Temizle, LONG: Çıkış
"""
import collections, time
from pathlib import Path
from core.framebuffer import Framebuffer

METRICS = ["CPU %", "RAM %", "Sicaklik"]

class GraphApp:
    NAME = "graph"; LABEL = "Graf"; ICON = "graph"

    def __init__(self, on_exit):
        self.on_exit = on_exit; self._metric = 0
        self.history = collections.deque(maxlen=100)
        self._cpu_prev = (0, 0); self._last = 0

    def on_up(self): self._metric = (self._metric - 1) % len(METRICS); self.history.clear()
    def on_down(self): self._metric = (self._metric + 1) % len(METRICS); self.history.clear()
    def on_sel(self): self.history.clear()
    def on_long(self): self.on_exit()

    def _read_cpu(self):
        try:
            line = Path("/proc/stat").read_text().split("\n")[0].split()
            vals = list(map(int, line[1:8]))
            idle, total = vals[3], sum(vals)
            pi, pt = self._cpu_prev; di, dt = idle-pi, total-pt
            self._cpu_prev = (idle, total)
            return max(0, min(100, 100-int(100*di/dt))) if dt else 0
        except: return 0

    def _read_ram(self):
        try:
            d = {}
            for l in Path("/proc/meminfo").read_text().split("\n"):
                p = l.split()
                if len(p)>=2: d[p[0].rstrip(":")]=int(p[1])
            t=d.get("MemTotal",1); f=d.get("MemAvailable",t)
            return int(100*(t-f)/t)
        except: return 0

    def _read_temp(self):
        try: return int(Path("/sys/class/thermal/thermal_zone0/temp").read_text().strip())//1000
        except: return 0

    def update(self):
        now = time.monotonic()
        if now - self._last < 1.0: return
        self._last = now
        if self._metric == 0: self.history.append(self._read_cpu())
        elif self._metric == 1: self.history.append(self._read_ram())
        else: self.history.append(self._read_temp())

    def draw(self, fb: Framebuffer):
        name = METRICS[self._metric]
        fb.icon("graph", 1, 10); fb.text(name, 12, 10)
        fb.hline(0, 18, 128)
        gx, gy, gw, gh = 14, 20, 100, 32
        mx = 100 if self._metric < 2 else 90
        fb.rect(gx-1, gy-1, gw+2, gh+2)
        fb.text(str(mx), 1, gy); fb.text("0", 5, gy+gh-7)
        if len(self.history) > 1:
            for i in range(len(self.history)-1):
                v0, v1 = self.history[i], self.history[i+1]
                y0 = gy+gh-int(v0*gh/mx); y1 = gy+gh-int(v1*gh/mx)
                y0 = max(gy, min(gy+gh, y0)); y1 = max(gy, min(gy+gh, y1))
                fb.line(gx+i, y0, gx+i+1, y1)
        if self.history:
            fb.text(f"{self.history[-1]}", 118, gy+gh//2-3)
        fb.text("[UP/DN]Metrik", 1, 56)
