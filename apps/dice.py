"""
TinyOLED Desktop — Zar Simülatörü
UP/DOWN: Zar tipi, SEL: At, LONG: Çıkış
"""
import random, time
from core.framebuffer import Framebuffer

DICE_TYPES = [4, 6, 8, 10, 12, 20]

class DiceApp:
    NAME = "dice"; LABEL = "Zar"; ICON = "dice"

    def __init__(self, on_exit):
        self.on_exit = on_exit; self._type_idx = 1; self.result = 0
        self._rolling = False; self._roll_frames = 0; self._last = 0

    def on_up(self): self._type_idx = (self._type_idx - 1) % len(DICE_TYPES)
    def on_down(self): self._type_idx = (self._type_idx + 1) % len(DICE_TYPES)
    def on_sel(self):
        if not self._rolling:
            self._rolling = True; self._roll_frames = 0
    def on_long(self): self.on_exit()

    def update(self):
        if not self._rolling: return
        now = time.monotonic()
        if now - self._last < 0.05: return
        self._last = now
        self._roll_frames += 1
        sides = DICE_TYPES[self._type_idx]
        self.result = random.randint(1, sides)
        if self._roll_frames >= 20: self._rolling = False

    def draw(self, fb: Framebuffer):
        sides = DICE_TYPES[self._type_idx]
        fb.text(f"Zar: D{sides}", 2, 10)
        fb.hline(0, 18, 128)
        # Zar tipi göstergesi
        for i, d in enumerate(DICE_TYPES):
            x = 4 + i * 21; sel = (i == self._type_idx)
            if sel: fb.rect(x-1, 20, 20, 10, fill=True)
            fb.text(f"D{d}", x, 21, on=not sel)
        # Büyük sonuç
        if self.result > 0:
            r_str = str(self.result)
            scale = 4
            total_w = len(r_str) * 6 * scale
            sx = (128 - total_w) // 2
            for ch in r_str:
                from core.font import Font
                cols = Font.glyph(ch)
                for ci, col in enumerate(cols):
                    for ri in range(7):
                        if col & (1 << ri):
                            fb.rect(sx+ci*scale, 34+ri*scale, scale, scale, fill=True)
                sx += 6 * scale
        if self._rolling:
            fb.text_centered("Yuvarlanıyor...", 56)
        else:
            fb.text("[SEL] At", 2, 56)
