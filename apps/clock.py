"""
TinyOLED Desktop — Saat & Takvim Uygulaması
Tam ekran analog saat simülasyonu (daire + ibreler)
ve dijital saat/tarih gösterimi.

Düğmeler:
  UP   → Analog / Dijital mod değiştir
  DOWN → (kullanılmıyor)
  SEL  → Geri (launcher'a dön)
"""

import math
import time
from core.framebuffer import Framebuffer
from core.font import Font

CONTENT_Y = 10
CLOCK_CX  = 64     # Analog saat merkezi X
CLOCK_CY  = 35     # Analog saat merkezi Y
CLOCK_R   = 22     # Analog saat yarıçapı


class ClockApp:
    NAME  = "clock"
    LABEL = "Saat"
    ICON  = "clock"

    def __init__(self, on_exit):
        self.on_exit  = on_exit
        self.mode     = "digital"   # "digital" | "analog"
        self._tick    = 0

    def on_up(self):
        """Modu değiştir."""
        self.mode = "analog" if self.mode == "digital" else "digital"

    def on_down(self):
        pass

    def on_sel(self):
        self.on_exit()

    def on_long(self):
        self.on_exit()

    def update(self):
        self._tick += 1

    def draw(self, fb: Framebuffer):
        now = time.localtime()
        if self.mode == "digital":
            self._draw_digital(fb, now)
        else:
            self._draw_analog(fb, now)

    # ── Dijital Mod ───────────────────────────────────────────
    def _draw_digital(self, fb: Framebuffer, t):
        # Büyük saat (6× font → 30×42 px)
        h_str = f"{t.tm_hour:02d}"
        m_str = f"{t.tm_min:02d}"
        s_str = f"{t.tm_sec:02d}"

        # Saati 2× scale ile çiz (her piksel 2×2 blok)
        self._big_text(fb, h_str, 4, CONTENT_Y + 4, scale=3)
        self._big_text(fb, ":", 4 + 2 * 6 * 3 + 1, CONTENT_Y + 4, scale=3)
        self._big_text(fb, m_str, 4 + 2 * 6 * 3 + 6, CONTENT_Y + 4, scale=3)

        # Saniyeler
        fb.text(f":{s_str}", 110, CONTENT_Y + 20)

        # Tarih satırı
        days   = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        months = ["Oca", "Şub", "Mar", "Nis", "May", "Haz",
                  "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
        day_name  = days[t.tm_wday]
        month_name= months[t.tm_mon - 1]
        date_str  = f"{day_name} {t.tm_mday} {month_name} {t.tm_year}"
        fb.text_centered(date_str, CONTENT_Y + 36)

        # Mod değiştirme ipucu
        fb.text("[UP]mod", 1, 56)

    def _big_text(self, fb: Framebuffer, text: str, x: int, y: int, scale: int = 2):
        """scale× büyütülmüş metin."""
        cx = x
        for char in text:
            cols = Font.glyph(char)
            for ci, col_byte in enumerate(cols):
                for ri in range(Font.CHAR_H):
                    if col_byte & (1 << ri):
                        fb.rect(cx + ci * scale, y + ri * scale,
                                scale, scale, fill=True)
            cx += (Font.CHAR_W + Font.CHAR_SPACING) * scale

    # ── Analog Mod ────────────────────────────────────────────
    def _draw_analog(self, fb: Framebuffer, t):
        cx, cy, r = CLOCK_CX, CLOCK_CY, CLOCK_R

        # Kadran
        fb.circle(cx, cy, r)

        # Saat işaretleri
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            outer_x = int(cx + (r - 1) * math.cos(angle))
            outer_y = int(cy + (r - 1) * math.sin(angle))
            inner_x = int(cx + (r - 3) * math.cos(angle))
            inner_y = int(cy + (r - 3) * math.sin(angle))
            fb.line(inner_x, inner_y, outer_x, outer_y)

        # Dakika ibreleri (ince, uzun)
        min_angle = math.radians(t.tm_min * 6 - 90)
        mx = int(cx + (r - 5) * math.cos(min_angle))
        my = int(cy + (r - 5) * math.sin(min_angle))
        fb.line(cx, cy, mx, my)

        # Saat ibreleri (kalın, kısa)
        hour_angle = math.radians((t.tm_hour % 12) * 30 + t.tm_min * 0.5 - 90)
        hx = int(cx + (r - 10) * math.cos(hour_angle))
        hy = int(cy + (r - 10) * math.sin(hour_angle))
        fb.line(cx, cy, hx, hy)
        fb.line(cx + 1, cy, hx + 1, hy)    # kalınlık için

        # Saniye ibresi (noktalı)
        sec_angle = math.radians(t.tm_sec * 6 - 90)
        sx = int(cx + (r - 3) * math.cos(sec_angle))
        sy = int(cy + (r - 3) * math.sin(sec_angle))
        for step in range(0, r - 3, 2):
            px = int(cx + step * math.cos(sec_angle))
            py = int(cy + step * math.sin(sec_angle))
            fb.pixel(px, py)

        # Merkez nokta
        fb.circle(cx, cy, 2, fill=True)

        # Dijital saat (sağ taraf)
        fb.text(f"{t.tm_hour:02d}:{t.tm_min:02d}", 96, CONTENT_Y + 4)
        fb.text(f":{t.tm_sec:02d}", 96, CONTENT_Y + 14)

        # Tarih
        fb.text(f"{t.tm_mday:02d}/{t.tm_mon:02d}", 96, CONTENT_Y + 28)
        fb.text(str(t.tm_year), 96, CONTENT_Y + 38)

        fb.text("[UP]mod", 1, 56)
