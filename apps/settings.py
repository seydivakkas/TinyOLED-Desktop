"""
TinyOLED Desktop — Sistem Ayarları
Parlaklık, kontras, ekran zaman aşımı, hostname,
tarih/saat ayarları.

Düğmeler:
  UP   → Önceki ayar
  DOWN → Sonraki ayar
  SEL  → Değeri değiştir (+)
  LONG → Geri
"""

import json
import subprocess
from pathlib import Path
from typing import List, Any, Callable

from core.framebuffer import Framebuffer
from core.font import Font
from core.display import SSD1306

CONTENT_Y = 10
LINE_H    = Font.CHAR_H + 2
CONFIG    = Path("/home/pi/tiny-oled-desktop/config/config.json")


def _load_config() -> dict:
    try:
        return json.loads(CONFIG.read_text())
    except Exception:
        return {}


def _save_config(data: dict):
    try:
        CONFIG.write_text(json.dumps(data, indent=2))
    except Exception:
        pass


class Setting:
    def __init__(self, key: str, label: str,
                 min_val, max_val, step, unit: str = "",
                 on_change: Callable = None):
        self.key       = key
        self.label     = label
        self.min_val   = min_val
        self.max_val   = max_val
        self.step      = step
        self.unit      = unit
        self.on_change = on_change
        self.value     = min_val

    def increment(self):
        self.value = min(self.max_val, self.value + self.step)
        if self.on_change:
            self.on_change(self.value)

    def decrement(self):
        self.value = max(self.min_val, self.value - self.step)
        if self.on_change:
            self.on_change(self.value)

    @property
    def display(self) -> str:
        return f"{self.value}{self.unit}"


class SettingsApp:
    NAME  = "settings"
    LABEL = "Ayar"
    ICON  = "gear"

    def __init__(self, on_exit, notify, display: SSD1306):
        self.on_exit = on_exit
        self.notify  = notify
        self._display = display
        self._cursor  = 0
        self._scroll  = 0
        self._config  = _load_config()
        self._settings: List[Setting] = self._build_settings()
        self._load_values()

    def _build_settings(self) -> List[Setting]:
        return [
            Setting(
                "brightness", "Parlaklik",
                min_val=10, max_val=255, step=25, unit="",
                on_change=lambda v: self._display.brightness(v),
            ),
            Setting(
                "timeout_s", "Ekran Timeout",
                min_val=10, max_val=300, step=10, unit="s",
            ),
            Setting(
                "contrast", "Kontrast",
                min_val=0, max_val=3, step=1, unit="",
            ),
            Setting(
                "fps", "FPS",
                min_val=5, max_val=30, step=5, unit="fps",
            ),
        ]

    def _load_values(self):
        for s in self._settings:
            s.value = self._config.get(s.key, s.min_val)

    def _save(self):
        for s in self._settings:
            self._config[s.key] = s.value
        _save_config(self._config)
        self.notify("Kaydedildi!")

    def on_up(self):
        if self._cursor > 0:
            self._cursor -= 1
            if self._cursor < self._scroll:
                self._scroll -= 1

    def on_down(self):
        if self._cursor < len(self._settings) - 1:
            self._cursor += 1
            max_lines = (54 - CONTENT_Y - 10) // LINE_H
            if self._cursor >= self._scroll + max_lines:
                self._scroll += 1

    def on_sel(self):
        """SEL → değeri artır; max'a gelince min'e döner."""
        s = self._settings[self._cursor]
        if s.value >= s.max_val:
            s.value = s.min_val
        else:
            s.increment()
        self._save()

    def on_long(self):
        self.on_exit()

    def update(self):
        pass

    # ── Çizim ─────────────────────────────────────────────────
    def draw(self, fb: Framebuffer):
        fb.icon("gear", 1, CONTENT_Y)
        fb.text("Ayarlar", 12, CONTENT_Y)
        fb.hline(0, CONTENT_Y + 9, 128)

        y         = CONTENT_Y + 11
        max_lines = (54 - y) // LINE_H

        visible = self._settings[self._scroll: self._scroll + max_lines]

        for idx, setting in enumerate(visible):
            abs_idx  = self._scroll + idx
            selected = (abs_idx == self._cursor)

            if selected:
                fb.rect(0, y - 1, 128, LINE_H + 1, fill=True)

            label_str = setting.label[:10]
            val_str   = setting.display
            fb.text(label_str, 1, y, on=not selected)
            fb.text(val_str, 128 - Font.text_width(val_str) - 2, y, on=not selected)

            # Mini progress bar (ayar aralığını göster)
            if not selected:
                total_range = setting.max_val - setting.min_val
                cur_range   = setting.value - setting.min_val
                bar_w = 40
                bar_x = 80
                fb.rect(bar_x, y + 1, bar_w, 4)
                fw = int(bar_w * cur_range / total_range) if total_range else 0
                if fw > 0:
                    fb.rect(bar_x + 1, y + 2, fw - 1, 2, fill=True)

            y += LINE_H

        # İpuçları
        fb.text("SEL:degistir", 1, 56)
        fb.text("LONG:geri", 82, 56)
