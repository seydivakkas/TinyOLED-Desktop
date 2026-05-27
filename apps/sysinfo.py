"""
TinyOLED Desktop — Sistem Monitörü
CPU yüzdesi, RAM, sıcaklık, uptime, disk ve ağ istatistiklerini gösterir.

Düğmeler:
  UP   → Önceki sayfa
  DOWN → Sonraki sayfa
  SEL  → Geri (launcher'a dön)
  LONG → Geri
"""

import subprocess
import time
from pathlib import Path
from typing import List, Tuple

from core.framebuffer import Framebuffer
from core.font import Font

CONTENT_Y = 10
LINE_H    = Font.CHAR_H + 2   # 9 piksel satır yüksekliği
MAX_LINES = (54 - CONTENT_Y) // LINE_H   # ~4 satır


def _read(path: str, default: str = "0") -> str:
    try:
        return Path(path).read_text().strip()
    except Exception:
        return default


def _run(cmd: List[str]) -> str:
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL,
                                       text=True).strip()
    except Exception:
        return "?"


class SysInfoApp:
    NAME  = "sysinfo"
    LABEL = "Sistem"
    ICON  = "cpu"

    PAGES = ["cpu_ram", "temp_disk", "network", "uptime"]

    def __init__(self, on_exit):
        self.on_exit   = on_exit
        self._page     = 0
        self._data     = {}
        self._cpu_prev = (0, 0)
        self.update()

    def on_up(self):
        self._page = (self._page - 1) % len(self.PAGES)

    def on_down(self):
        self._page = (self._page + 1) % len(self.PAGES)

    def on_sel(self):
        self.on_exit()

    def on_long(self):
        self.on_exit()

    # ── Veri Toplama ──────────────────────────────────────────
    def update(self):
        self._collect_cpu()
        self._collect_mem()
        self._collect_temp()
        self._collect_disk()
        self._collect_net()
        self._collect_uptime()

    def _collect_cpu(self):
        try:
            line  = Path("/proc/stat").read_text().split("\n")[0].split()
            vals  = list(map(int, line[1:8]))
            idle  = vals[3]
            total = sum(vals)
            prev_idle, prev_total = self._cpu_prev
            d_idle  = idle  - prev_idle
            d_total = total - prev_total
            pct = 0 if d_total == 0 else 100 - int(100 * d_idle / d_total)
            self._data["cpu_pct"] = max(0, min(100, pct))
            self._cpu_prev = (idle, total)
        except Exception:
            self._data["cpu_pct"] = 0

    def _collect_mem(self):
        try:
            lines = Path("/proc/meminfo").read_text().split("\n")
            vals  = {}
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    vals[parts[0].rstrip(":")] = int(parts[1])
            total   = vals.get("MemTotal", 1)
            free    = vals.get("MemAvailable", total)
            used    = total - free
            self._data["mem_total"] = total // 1024     # MB
            self._data["mem_used"]  = used  // 1024
            self._data["mem_pct"]   = int(100 * used / total)
        except Exception:
            self._data.update({"mem_total": 0, "mem_used": 0, "mem_pct": 0})

    def _collect_temp(self):
        raw = _read("/sys/class/thermal/thermal_zone0/temp", "0")
        try:
            self._data["temp_c"] = int(raw) // 1000
        except ValueError:
            self._data["temp_c"] = 0

    def _collect_disk(self):
        try:
            out   = _run(["df", "-h", "/"])
            lines = out.split("\n")
            if len(lines) >= 2:
                parts = lines[1].split()
                self._data["disk_total"] = parts[1] if len(parts) > 1 else "?"
                self._data["disk_used"]  = parts[2] if len(parts) > 2 else "?"
                self._data["disk_pct"]   = parts[4] if len(parts) > 4 else "?"
            else:
                self._data.update({"disk_total": "?", "disk_used": "?", "disk_pct": "?"})
        except Exception:
            self._data.update({"disk_total": "?", "disk_used": "?", "disk_pct": "?"})

    def _collect_net(self):
        try:
            lines = Path("/proc/net/dev").read_text().split("\n")
            for line in lines:
                if "wlan0" in line:
                    parts = line.split()
                    rx_mb = int(parts[1]) // (1024 * 1024)
                    tx_mb = int(parts[9]) // (1024 * 1024)
                    self._data["rx_mb"] = rx_mb
                    self._data["tx_mb"] = tx_mb
                    return
            self._data.update({"rx_mb": 0, "tx_mb": 0})
        except Exception:
            self._data.update({"rx_mb": 0, "tx_mb": 0})

    def _collect_uptime(self):
        try:
            secs   = float(Path("/proc/uptime").read_text().split()[0])
            h, rem = divmod(int(secs), 3600)
            m, s   = divmod(rem, 60)
            self._data["uptime"] = f"{h:02d}:{m:02d}:{s:02d}"
        except Exception:
            self._data["uptime"] = "?:??:??"

    # ── Çizim ─────────────────────────────────────────────────
    def draw(self, fb: Framebuffer):
        page = self.PAGES[self._page]

        if page == "cpu_ram":
            self._draw_cpu_ram(fb)
        elif page == "temp_disk":
            self._draw_temp_disk(fb)
        elif page == "network":
            self._draw_network(fb)
        elif page == "uptime":
            self._draw_uptime(fb)

        # Sayfa göstergesi
        total = len(self.PAGES)
        for p in range(total):
            px = 128 // 2 - total * 3 + p * 6
            if p == self._page:
                fb.rect(px, 58, 4, 3, fill=True)
            else:
                fb.rect(px, 58, 4, 3)

    def _draw_cpu_ram(self, fb: Framebuffer):
        fb.icon("cpu", 1, CONTENT_Y)
        fb.text("CPU & RAM", 12, CONTENT_Y)
        y = CONTENT_Y + 10

        # CPU
        cpu = self._data.get("cpu_pct", 0)
        fb.text(f"CPU: {cpu:3d}%", 1, y)
        fb.progress_bar(50, y, 76, 7, cpu)
        y += LINE_H + 1

        # RAM
        mu  = self._data.get("mem_used",  0)
        mt  = self._data.get("mem_total", 1)
        mp  = self._data.get("mem_pct",   0)
        fb.text(f"RAM: {mu}/{mt}MB", 1, y)
        y += LINE_H
        fb.progress_bar(1, y, 126, 7, mp)

    def _draw_temp_disk(self, fb: Framebuffer):
        fb.icon("temp", 1, CONTENT_Y)
        fb.text("Isı & Disk", 12, CONTENT_Y)
        y = CONTENT_Y + 10

        temp = self._data.get("temp_c", 0)
        warn = " !!" if temp > 70 else ""
        fb.text(f"Sicak: {temp}C{warn}", 1, y)
        y += LINE_H

        # Sıcaklık bar (maks 90°C)
        fb.progress_bar(1, y, 126, 7, temp, max_val=90)
        y += LINE_H + 1

        # Disk
        du = self._data.get("disk_used",  "?")
        dt = self._data.get("disk_total", "?")
        dp = self._data.get("disk_pct",   "?")
        fb.icon("folder", 1, y)
        fb.text(f"{du}/{dt} ({dp})", 12, y + 1)

    def _draw_network(self, fb: Framebuffer):
        fb.icon("wifi", 1, CONTENT_Y)
        fb.text("Ag", 12, CONTENT_Y)
        y = CONTENT_Y + 10

        rx = self._data.get("rx_mb", 0)
        tx = self._data.get("tx_mb", 0)
        fb.text(f"RX: {rx} MB", 1, y);  y += LINE_H
        fb.text(f"TX: {tx} MB", 1, y);  y += LINE_H

        # IP adresi
        ip = _run(["hostname", "-I"]).split()
        fb.text(ip[0] if ip else "bagli degil", 1, y)

    def _draw_uptime(self, fb: Framebuffer):
        fb.icon("heart", 1, CONTENT_Y)
        fb.text("Uptime", 12, CONTENT_Y)
        y = CONTENT_Y + 12

        fb.text_centered(self._data.get("uptime", "?"), y)
        y += LINE_H + 4

        # Hostname
        hn = _run(["hostname"])
        fb.text(f"Host: {hn[:16]}", 1, y)
        y += LINE_H

        # Kernel
        kr = _run(["uname", "-r"])
        fb.text(kr[:21], 1, y)
