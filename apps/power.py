"""
TinyOLED Desktop — Güç Yönetimi Menüsü
Yeniden başlat, kapat, ekranı uyut seçenekleri.

Düğmeler:
  UP   → Yukarı
  DOWN → Aşağı
  SEL  → Onayla (2. basışta gerçekleşir)
  LONG → Geri
"""

import os
import subprocess
import time
from typing import List, Tuple

from core.framebuffer import Framebuffer
from core.font import Font

CONTENT_Y = 10


class PowerOption:
    def __init__(self, label: str, icon: str, confirm_label: str, action):
        self.label         = label
        self.icon          = icon
        self.confirm_label = confirm_label
        self.action        = action


class PowerApp:
    NAME  = "power"
    LABEL = "Guc"
    ICON  = "power"

    def __init__(self, on_exit, notify, display):
        self.on_exit  = on_exit
        self.notify   = notify
        self._display = display
        self._cursor  = 0
        self._confirm = False   # Onay bekleniyor mu?
        self._options: List[PowerOption] = [
            PowerOption(
                "Yeniden Baslat", "power",
                "EMIN MISINIZ?",
                lambda: subprocess.run(["sudo", "reboot"])
            ),
            PowerOption(
                "Kapat", "power",
                "EMIN MISINIZ?",
                lambda: subprocess.run(["sudo", "halt"])
            ),
            PowerOption(
                "Ekrani Uyut", "lock",
                "Ekran kapanacak",
                self._sleep_display
            ),
            PowerOption(
                "Geri Don", "arrow_right",
                "",
                on_exit
            ),
        ]

    def _sleep_display(self):
        self._display.power(False)
        time.sleep(5)
        self._display.power(True)
        self.on_exit()

    def on_up(self):
        if self._confirm:
            self._confirm = False
            return
        self._cursor = (self._cursor - 1) % len(self._options)

    def on_down(self):
        if self._confirm:
            self._confirm = False
            return
        self._cursor = (self._cursor + 1) % len(self._options)

    def on_sel(self):
        opt = self._options[self._cursor]
        if opt.confirm_label and not self._confirm:
            self._confirm = True
        else:
            self._confirm = False
            opt.action()

    def on_long(self):
        if self._confirm:
            self._confirm = False
        else:
            self.on_exit()

    def update(self):
        pass

    # ── Çizim ─────────────────────────────────────────────────
    def draw(self, fb: Framebuffer):
        fb.icon("power", 1, CONTENT_Y)
        fb.text("Guc Secenekleri", 12, CONTENT_Y)
        fb.hline(0, CONTENT_Y + 9, 128)

        if self._confirm:
            self._draw_confirm(fb)
            return

        y      = CONTENT_Y + 12
        line_h = Font.CHAR_H + 4

        for idx, opt in enumerate(self._options):
            selected = (idx == self._cursor)
            if selected:
                fb.rounded_rect(0, y - 2, 128, line_h, r=2, fill=True)

            fb.icon(opt.icon, 2, y - 1, on=not selected)
            fb.text(opt.label, 14, y, on=not selected)
            y += line_h

        fb.text("SEL:sec LONG:geri", 1, 56)

    def _draw_confirm(self, fb: Framebuffer):
        opt = self._options[self._cursor]
        fb.rect(10, 20, 108, 28, fill=False)
        fb.rect(11, 21, 106, 26, fill=True)

        fb.text_centered(opt.confirm_label, 24, on=False)
        fb.text_centered(opt.label,         32, on=False)
        fb.text_centered("SEL:evet LONG:iptal", 52)
