"""
TinyOLED Desktop — Flappy Bird Klonu
UP/SEL: Zıpla, LONG: Çıkış
"""
import random, time
from core.framebuffer import Framebuffer

class FlappyApp:
    NAME = "flappy"; LABEL = "Flappy"; ICON = "bird"

    def __init__(self, on_exit):
        self.on_exit = on_exit; self.reset()

    def reset(self):
        self.bird_y = 32.0; self.vel = 0.0; self.gravity = 0.8
        self.pipes = []; self.score = 0; self.game_over = False
        self.frame = 0; self._last = 0
        self._add_pipe(128)

    def _add_pipe(self, x):
        gap_y = random.randint(18, 46); gap_h = 20
        self.pipes.append({"x": x, "gap_y": gap_y, "gap_h": gap_h, "scored": False})

    def _flap(self):
        if self.game_over: return
        self.vel = -4.5

    def on_up(self): self._flap()
    def on_down(self): pass
    def on_sel(self):
        if self.game_over: self.reset()
        else: self._flap()
    def on_long(self): self.on_exit()

    def update(self):
        if self.game_over: return
        now = time.monotonic()
        if now - self._last < 0.05: return
        self._last = now
        self.vel += self.gravity; self.bird_y += self.vel
        bird_x, bird_r = 20, 3
        if self.bird_y < 10 or self.bird_y > 62:
            self.game_over = True; return
        for p in self.pipes:
            p["x"] -= 2
            if not p["scored"] and p["x"] < bird_x:
                p["scored"] = True; self.score += 1
            if p["x"] + 6 > bird_x - bird_r and p["x"] < bird_x + bird_r:
                by = int(self.bird_y)
                if by - bird_r < p["gap_y"] or by + bird_r > p["gap_y"] + p["gap_h"]:
                    self.game_over = True; return
        self.pipes = [p for p in self.pipes if p["x"] > -10]
        if not self.pipes or self.pipes[-1]["x"] < 80:
            self._add_pipe(130)

    def draw(self, fb: Framebuffer):
        fb.text(f"Skor:{self.score}", 50, 2)
        if self.game_over:
            fb.text_centered("GAME OVER", 24)
            fb.text_centered(f"Skor: {self.score}", 34)
            fb.text_centered("[SEL] Tekrar", 46)
            return
        by = int(self.bird_y)
        fb.circle(20, by, 3, fill=True)
        fb.pixel(24, by-1); fb.pixel(24, by)
        for p in self.pipes:
            px = int(p["x"])
            fb.rect(px, 10, 6, p["gap_y"]-10, fill=True)
            fb.rect(px, p["gap_y"]+p["gap_h"], 6, 64-p["gap_y"]-p["gap_h"], fill=True)
        fb.hline(0, 9, 128)
