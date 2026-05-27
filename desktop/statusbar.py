"""
TinyOLED Desktop — Üst Durum Çubuğu (Status Bar)
128 × 8 piksel şerit — en üstte her zaman görünür.

Gösterir:
  [Saat 12:34] ··· [WiFi ikon] [Sıcaklık] [CPU%] [Batarya]
"""

import subprocess
import time
from pathlib import Path
from typing import Optional

from core.framebuffer import Framebuffer
from core.font import Font


BAR_H = 9   # status bar piksel yüksekliği (8 karakter + 1 ayıraç)


def _read_file(path: str, default: str = "?") -> str:
    try:
        return Path(path).read_text().strip()
    except Exception:
        return default


class StatusBar:
    """
    Durum çubuğu verilerini toplar ve framebuffer üzerine çizer.
    Her saniye `update()` çağrılarak veriler tazelenir.
    """

    def __init__(self):
        self.time_str   = "00:00"
        self.cpu_pct    = 0
        self.temp_c     = 0
        self.batt_pct   = 100
        self.wifi_ok    = False
        self.wifi_ssid  = ""
        self._last_cpu_idle  = 0
        self._last_cpu_total = 0

    # ── Veri Güncelleme ────────────────────────────────────────
    def update(self):
        """Tüm durum verilerini yenile (saniyede bir çağrılır)."""
        self._update_time()
        self._update_cpu()
        self._update_temp()
        self._update_wifi()
        self._update_battery()

    def _update_time(self):
        self.time_str = time.strftime("%H:%M")

    def _update_cpu(self):
        """Basit /proc/stat okuması ile CPU yüzdesi."""
        try:
            line = Path("/proc/stat").read_text().split("\n")[0].split()
            # user, nice, system, idle, iowait, irq, softirq
            vals  = list(map(int, line[1:8]))
            idle  = vals[3]
            total = sum(vals)
            d_idle  = idle  - self._last_cpu_idle
            d_total = total - self._last_cpu_total
            if d_total > 0:
                self.cpu_pct = max(0, min(100, 100 - int(100 * d_idle / d_total)))
            self._last_cpu_idle  = idle
            self._last_cpu_total = total
        except Exception:
            self.cpu_pct = 0

    def _update_temp(self):
        """CPU sıcaklığını /sys üzerinden oku (Raspberry Pi)."""
        raw = _read_file("/sys/class/thermal/thermal_zone0/temp", "0")
        try:
            self.temp_c = int(raw) // 1000
        except ValueError:
            self.temp_c = 0

    def _update_wifi(self):
        """WiFi bağlantı durumu."""
        try:
            out = subprocess.check_output(
                ["iwgetid", "-r"], stderr=subprocess.DEVNULL, text=True
            ).strip()
            self.wifi_ok   = bool(out)
            self.wifi_ssid = out
        except Exception:
            self.wifi_ok   = False
            self.wifi_ssid = ""

    def _update_battery(self):
        """
        Raspberry Pi normalde batarya taşımaz.
        UPS-pHAT veya benzer bir modül takılıysa
        /sys/class/power_supply/BAT0/capacity okunur.
        """
        raw = _read_file("/sys/class/power_supply/BAT0/capacity", "-1")
        try:
            self.batt_pct = int(raw)
        except ValueError:
            self.batt_pct = -1   # batarya yok

    # ── Çizim ─────────────────────────────────────────────────
    def draw(self, fb: Framebuffer):
        """
        Framebuffer'ın en üstüne 9 piksellik şerit çizer.
        Çağrıldığında fb.clear() yapılmış olmalı.
        """
        # Arkaplan çizgisi
        fb.hline(0, BAR_H - 1, 128, True)

        # ── Sol: Saat ─────────────────────────────────────────
        fb.text(self.time_str, 1, 1)

        # ── Sağ: İkonlar (sağdan sola) ──────────────────────
        x = 126

        # Batarya (sadece modül takılıysa)
        if self.batt_pct >= 0:
            batt_str = f"{self.batt_pct}%"
            x -= Font.text_width(batt_str)
            fb.text(batt_str, x, 1)
            x -= 2

        # Sıcaklık
        temp_str = f"{self.temp_c}C"
        x -= Font.text_width(temp_str)
        fb.text(temp_str, x, 1)
        x -= 2

        # CPU
        cpu_str = f"{self.cpu_pct}%"
        x -= Font.text_width(cpu_str)
        fb.text(cpu_str, x, 1)
        x -= 3

        # WiFi ikonu (8px geniş)
        x -= 8
        if self.wifi_ok:
            fb.icon("wifi", x, 0)
        else:
            # Üzeri çizgili X
            fb.icon("wifi", x, 0)
            fb.line(x, 0, x + 7, 7)   # diagonal X
