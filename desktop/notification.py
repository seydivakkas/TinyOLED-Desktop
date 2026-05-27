"""
TinyOLED Desktop — Bildirim Sistemi
Ekranın altında kısa süreli mesajlar gösterir.

Kullanım:
    notif = NotificationManager()
    notif.push("WiFi bağlandı!", duration=2.5)
"""

import time
from typing import Optional
from core.framebuffer import Framebuffer
from core.font import Font


NOTIF_Y = 55   # bildirim şeridinin Y konumu (alt)
NOTIF_H = 9    # yükseklik


class Notification:
    def __init__(self, message: str, duration: float = 2.0):
        self.message  = message
        self.duration = duration
        self.created  = time.monotonic()

    def is_expired(self) -> bool:
        return (time.monotonic() - self.created) >= self.duration

    def progress(self) -> float:
        """0.0 → 1.0 yaşam süreci."""
        return min(1.0, (time.monotonic() - self.created) / self.duration)


class NotificationManager:
    def __init__(self):
        self._current: Optional[Notification] = None
        self._queue: list = []

    def push(self, message: str, duration: float = 2.5):
        """Yeni bildirim ekle."""
        n = Notification(message, duration)
        if self._current is None:
            self._current = n
        else:
            self._queue.append(n)

    def tick(self):
        """Her frame çağrılır; süresi dolmuşları kaldırır."""
        if self._current and self._current.is_expired():
            self._current = self._queue.pop(0) if self._queue else None

    def draw(self, fb: Framebuffer):
        """Aktif bildirimi framebuffer'a çiz."""
        if self._current is None:
            return

        n = self._current

        # Yarı saydam arka plan şeridi (invert region)
        fb.rect(0, NOTIF_Y, 128, NOTIF_H, on=True, fill=True)

        # Mesaj (beyaz metin siyah zemine = invert)
        max_chars = 128 // Font.CHAR_STRIDE
        msg = n.message[:max_chars]
        tw  = Font.text_width(msg)
        x   = max(1, (128 - tw) // 2)
        fb.text(msg, x, NOTIF_Y + 1, on=False)   # siyah metin, beyaz zemin

        # Alt progress bar
        bar_w = int(126 * (1.0 - n.progress()))
        if bar_w > 0:
            fb.hline(1, NOTIF_Y + NOTIF_H - 1, bar_w, on=False)

    @property
    def active(self) -> bool:
        return self._current is not None
