"""
TinyOLED Desktop — Yılan Oyunu
UP: Saat yönünde döndür, DOWN: Ters yön, SEL: Yeniden başlat, LONG: Çıkış
"""
import random, time
from core.framebuffer import Framebuffer

BLOCK = 4
AREA_Y = 10
AREA_H = 54

class SnakeApp:
    NAME = "snake"; LABEL = "Yilan"; ICON = "snake"

    def __init__(self, on_exit):
        self.on_exit = on_exit; self.reset()

    def reset(self):
        self.snake = [(64,32),(60,32),(56,32)]
        self.dir = (BLOCK, 0); self.food = self._rand_food()
        self.score = 0; self.game_over = False; self._last = 0

    def _rand_food(self):
        return (random.randint(2,30)*BLOCK, random.randint(3,14)*BLOCK)

    def on_up(self):
        if not self.game_over:
            dx,dy = self.dir; self.dir = (-dy, dx)
    def on_down(self):
        if not self.game_over:
            dx,dy = self.dir; self.dir = (dy, -dx)
    def on_sel(self):
        if self.game_over: self.reset()
    def on_long(self): self.on_exit()

    def update(self):
        if self.game_over: return
        now = time.monotonic()
        if now - self._last < 0.15: return
        self._last = now
        hx = (self.snake[0][0] + self.dir[0]) % 128
        hy = (self.snake[0][1] - AREA_Y + self.dir[1]) % AREA_H + AREA_Y
        head = (hx, hy)
        if head in self.snake:
            self.game_over = True; return
        self.snake.insert(0, head)
        if abs(hx-self.food[0])<BLOCK and abs(hy-self.food[1])<BLOCK:
            self.score += 1; self.food = self._rand_food()
        else:
            self.snake.pop()

    def draw(self, fb: Framebuffer):
        fb.text(f"Skor:{self.score}", 2, AREA_Y)
        fb.hline(0, AREA_Y+8, 128)
        if self.game_over:
            fb.text_centered("OYUN BITTI!", 28)
            fb.text_centered(f"Skor: {self.score}", 38)
            fb.text_centered("[SEL] Tekrar", 50)
            return
        fb.rect(self.food[0], self.food[1], BLOCK-1, BLOCK-1, fill=True)
        for i,(x,y) in enumerate(self.snake):
            fb.rect(x, y, BLOCK-1, BLOCK-1, fill=(i!=0))
