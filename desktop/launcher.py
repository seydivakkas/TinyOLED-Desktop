"""
TinyOLED Desktop — Uygulama Başlatıcı (App Launcher)
Status bar'ın altında 128×54 piksel alanda çalışır.

Düzen (3 sütun × 2 satır = 6 ikon):
  ┌──────────────────────────────────────────┐
  │  [CLK]  [SYS]  [WiFi]  [FILE] [SET] [PWR]│
  │  Saat   Sistem WiFi    Dosya  Ayar  Güç  │
  └──────────────────────────────────────────┘

Navigasyon:
  UP/DOWN → seçili ikonu kaydır
  SEL     → uygulamayı aç
"""

from typing import List, Callable, Optional
from core.framebuffer import Framebuffer
from core.font import Font

CONTENT_Y = 10   # status bar'ın altı
CONTENT_H = 44   # kullanılabilir yükseklik (notif yok iken)

COLS    = 3
ROWS    = 2
CELL_W  = 128 // COLS   # ~42 piksel
CELL_H  = CONTENT_H // ROWS  # ~22 piksel


class AppEntry:
    def __init__(self, name: str, label: str, icon: str, callback: Callable):
        self.name     = name
        self.label    = label
        self.icon     = icon      # 8×8 ikon adı (font.py içinde)
        self.callback = callback


class Launcher:
    """
    Ana ekran uygulama ızgarası.
    `select()` çağrıldığında ilgili app callback'i ateşlenir.
    """

    def __init__(self):
        self._apps: List[AppEntry] = []
        self._cursor: int = 0
        self._scroll: int = 0    # kaydırma (daha fazla uygulama için)
        self._anim_offset: int = 0   # seçim animasyonu

    def register(self, name: str, label: str, icon: str, callback: Callable):
        self._apps.append(AppEntry(name, label, icon, callback))

    def move_up(self):
        if self._cursor > 0:
            self._cursor -= 1
            self._anim_offset = 3

    def move_down(self):
        if self._cursor < len(self._apps) - 1:
            self._cursor += 1
            self._anim_offset = -3

    def select(self):
        if 0 <= self._cursor < len(self._apps):
            self._apps[self._cursor].callback()

    def current_app(self) -> Optional[AppEntry]:
        if 0 <= self._cursor < len(self._apps):
            return self._apps[self._cursor]
        return None

    def draw(self, fb: Framebuffer):
        """Uygulama ızgarasını çiz."""
        visible_start = (self._cursor // (COLS * ROWS)) * (COLS * ROWS)
        visible_apps  = self._apps[visible_start: visible_start + COLS * ROWS]

        for idx, app in enumerate(visible_apps):
            col = idx % COLS
            row = idx // COLS
            cx  = col * CELL_W
            cy  = CONTENT_Y + row * CELL_H
            abs_idx = visible_start + idx

            selected = (abs_idx == self._cursor)

            # Seçili hücre arka planı
            if selected:
                y_off = self._anim_offset
                fb.rounded_rect(cx + 1, cy + y_off, CELL_W - 2, CELL_H - 2,
                                r=2, on=True, fill=True)

            # İkon (hücre ortasında, 8×8)
            icon_x = cx + (CELL_W - 8) // 2
            icon_y = cy + 2
            fb.icon(app.icon, icon_x, icon_y, on=not selected)

            # Etiket (ikon altında, 5×7 font)
            label = app.label[:5]   # max 5 karakter (CELL_W sığdırmak için)
            lw    = Font.text_width(label)
            lx    = cx + (CELL_W - lw) // 2
            fb.text(label, lx, icon_y + 9, on=not selected)

        # Animasyon sönümle
        if self._anim_offset > 0:
            self._anim_offset -= 1
        elif self._anim_offset < 0:
            self._anim_offset += 1

        # Sayfa göstergesi (birden fazla sayfa varsa)
        total_pages = (len(self._apps) + COLS * ROWS - 1) // (COLS * ROWS)
        cur_page    = self._cursor // (COLS * ROWS)
        if total_pages > 1:
            for p in range(total_pages):
                px = 128 // 2 - total_pages * 3 + p * 6
                if p == cur_page:
                    fb.rect(px, CONTENT_Y + CONTENT_H + 1, 4, 2, fill=True)
                else:
                    fb.rect(px, CONTENT_Y + CONTENT_H + 1, 4, 2)
