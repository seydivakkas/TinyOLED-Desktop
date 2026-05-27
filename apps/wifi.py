"""
TinyOLED Desktop — WiFi Yöneticisi
Mevcut ağları listeler, bağlanır ve bağlantı keser.

Düğmeler:
  UP   → Yukarı kaydır
  DOWN → Aşağı kaydır
  SEL  → Seçili ağa bağlan
  LONG → Geri
"""

import subprocess
import threading
from typing import List, Optional, Tuple

from core.framebuffer import Framebuffer
from core.font import Font

CONTENT_Y = 10
LINE_H    = Font.CHAR_H + 2


class WiFiNetwork:
    def __init__(self, ssid: str, signal: int, secured: bool, connected: bool):
        self.ssid      = ssid
        self.signal    = signal     # -dBm (düşük = güçlü)
        self.secured   = secured
        self.connected = connected

    @property
    def bar_level(self) -> int:
        """0-4 çubuk (sinyal gücüne göre)."""
        if self.signal > -55:   return 4
        elif self.signal > -65: return 3
        elif self.signal > -75: return 2
        elif self.signal > -85: return 1
        return 0


class WiFiApp:
    NAME  = "wifi"
    LABEL = "WiFi"
    ICON  = "wifi"

    def __init__(self, on_exit, notify):
        self.on_exit   = on_exit
        self.notify    = notify
        self._networks: List[WiFiNetwork] = []
        self._cursor   = 0
        self._scroll   = 0
        self._scanning = False
        self._status   = "Taranıyor..."
        self._scan()

    def on_up(self):
        if self._cursor > 0:
            self._cursor -= 1
            if self._cursor < self._scroll:
                self._scroll = self._cursor

    def on_down(self):
        if self._cursor < len(self._networks) - 1:
            self._cursor += 1
            max_lines = (54 - CONTENT_Y) // LINE_H - 1
            if self._cursor >= self._scroll + max_lines:
                self._scroll = self._cursor - max_lines + 1

    def on_sel(self):
        if not self._networks:
            self._scan()
            return
        net = self._networks[self._cursor]
        if net.connected:
            self._disconnect()
        else:
            self._connect(net.ssid)

    def on_long(self):
        self.on_exit()

    def update(self):
        pass

    # ── Ağ İşlemleri ─────────────────────────────────────────
    def _scan(self):
        self._scanning = True
        self._status   = "Taranıyor..."
        threading.Thread(target=self._do_scan, daemon=True).start()

    def _do_scan(self):
        try:
            out = subprocess.check_output(
                ["sudo", "iwlist", "wlan0", "scan"],
                stderr=subprocess.DEVNULL, text=True
            )
            self._networks = self._parse_iwlist(out)
            self._status   = f"{len(self._networks)} ag bulundu"
        except Exception as e:
            self._networks = []
            self._status   = "Tarama hatasi"
        finally:
            self._scanning = False

    def _parse_iwlist(self, raw: str) -> List[WiFiNetwork]:
        nets   = []
        blocks = raw.split("Cell ")
        # Mevcut bağlı SSID'yi al
        try:
            connected_ssid = subprocess.check_output(
                ["iwgetid", "-r"], stderr=subprocess.DEVNULL, text=True
            ).strip()
        except Exception:
            connected_ssid = ""

        for block in blocks[1:]:
            ssid      = ""
            signal    = -100
            secured   = False

            for line in block.split("\n"):
                line = line.strip()
                if "ESSID:" in line:
                    ssid = line.split('"')[1] if '"' in line else ""
                elif "Signal level=" in line:
                    try:
                        sig_part = line.split("Signal level=")[1].split()[0]
                        signal   = int(sig_part.split("/")[0])
                    except Exception:
                        signal = -90
                elif "Encryption key:on" in line:
                    secured = True

            if ssid:
                nets.append(WiFiNetwork(
                    ssid      = ssid,
                    signal    = signal,
                    secured   = secured,
                    connected = (ssid == connected_ssid),
                ))

        # Bağlı olan ağı üste al
        nets.sort(key=lambda n: (not n.connected, -n.signal))
        return nets

    def _connect(self, ssid: str):
        self._status = f"Baglanıyor: {ssid[:12]}"
        def _do():
            try:
                subprocess.run(
                    ["sudo", "wpa_cli", "-i", "wlan0", "select_network",
                     self._get_network_id(ssid)],
                    timeout=10, check=True
                )
                self.notify(f"Baglandi: {ssid[:12]}")
            except Exception:
                self.notify("Baglanti hatasi!")
            self._scan()
        threading.Thread(target=_do, daemon=True).start()

    def _disconnect(self):
        try:
            subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "disconnect"],
                           check=True, timeout=5)
            self.notify("WiFi kesildi")
        except Exception:
            self.notify("Kesme hatasi!")
        self._scan()

    def _get_network_id(self, ssid: str) -> str:
        try:
            out = subprocess.check_output(
                ["sudo", "wpa_cli", "-i", "wlan0", "list_networks"],
                stderr=subprocess.DEVNULL, text=True
            )
            for line in out.split("\n")[1:]:
                parts = line.split("\t")
                if len(parts) >= 2 and parts[1] == ssid:
                    return parts[0]
        except Exception:
            pass
        return "0"

    # ── Çizim ─────────────────────────────────────────────────
    def draw(self, fb: Framebuffer):
        # Başlık
        fb.icon("wifi", 1, CONTENT_Y)
        status = "Taranıyor" if self._scanning else self._status
        fb.text(status[:18], 12, CONTENT_Y)
        fb.hline(0, CONTENT_Y + 9, 128)
        y = CONTENT_Y + 11

        if not self._networks:
            fb.text_centered("Ag bulunamadi" if not self._scanning
                             else "Lutfen bekleyin", y + 8)
            return

        max_lines = (54 - y) // LINE_H
        visible   = self._networks[self._scroll: self._scroll + max_lines]

        for idx, net in enumerate(visible):
            abs_idx  = self._scroll + idx
            selected = (abs_idx == self._cursor)

            if selected:
                fb.rect(0, y - 1, 128, LINE_H + 1, fill=True)

            # Sinyal çubukları (4 çubuk, sağda)
            bar_x = 118
            for b in range(4):
                bh = b + 2
                bx = bar_x + b * 3
                by = y + LINE_H - bh
                if b < net.bar_level:
                    fb.rect(bx, by, 2, bh, fill=True, on=not selected)
                else:
                    fb.rect(bx, by, 2, bh, fill=False, on=not selected)

            # Kilit ikonu
            lock_x = 108
            if net.secured:
                fb.icon("lock", lock_x, y - 1)

            # SSID
            max_ssid = 17 if net.secured else 20
            label    = net.ssid[:max_ssid]
            if net.connected:
                label = ">" + label
            fb.text(label, 1, y, on=not selected)

            y += LINE_H

        # Seçili ağ için ipucu
        if self._networks:
            net = self._networks[self._cursor]
            hint = "SEL:kes" if net.connected else "SEL:baglan"
            fb.text(hint, 1, 56)
            fb.text("LONG:geri", 80, 56)
