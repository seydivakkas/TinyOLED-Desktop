"""
TinyOLED Desktop — Dosya Tarayıcı
/home/pi ve / altındaki dosya sistemi navigasyonu.

Düğmeler:
  UP   → Yukarı
  DOWN → Aşağı
  SEL  → Dizine gir / dosya bilgisi göster
  LONG → Üst dizine çık / geri
"""

import os
import stat
from pathlib import Path
from typing import List, Tuple

from core.framebuffer import Framebuffer
from core.font import Font

CONTENT_Y = 10
LINE_H    = Font.CHAR_H + 2
START_DIR = "/home/pi"


class FileEntry:
    def __init__(self, name: str, path: str, is_dir: bool, size: int):
        self.name   = name
        self.path   = path
        self.is_dir = is_dir
        self.size   = size

    @property
    def size_str(self) -> str:
        if self.size < 1024:
            return f"{self.size}B"
        elif self.size < 1024 * 1024:
            return f"{self.size // 1024}K"
        else:
            return f"{self.size // (1024 * 1024)}M"


class FileBrowserApp:
    NAME  = "files"
    LABEL = "Dosya"
    ICON  = "folder"

    def __init__(self, on_exit, notify):
        self.on_exit = on_exit
        self.notify  = notify
        self._cwd    = START_DIR
        self._stack  = []        # geri navigasyon stack'i
        self._cursor = 0
        self._scroll = 0
        self._entries: List[FileEntry] = []
        self._info_mode = False  # dosya detay görünümü
        self._load_dir()

    def on_up(self):
        if self._info_mode:
            self._info_mode = False
            return
        if self._cursor > 0:
            self._cursor -= 1
            if self._cursor < self._scroll:
                self._scroll = self._cursor

    def on_down(self):
        if self._info_mode:
            return
        if self._cursor < len(self._entries) - 1:
            self._cursor += 1
            max_lines = (55 - CONTENT_Y - 10) // LINE_H
            if self._cursor >= self._scroll + max_lines:
                self._scroll += 1

    def on_sel(self):
        if self._info_mode:
            self._info_mode = False
            return
        if not self._entries:
            return
        entry = self._entries[self._cursor]
        if entry.is_dir:
            self._stack.append((self._cwd, self._cursor, self._scroll))
            self._cwd    = entry.path
            self._cursor = 0
            self._scroll = 0
            self._load_dir()
        else:
            self._info_mode = True

    def on_long(self):
        if self._info_mode:
            self._info_mode = False
            return
        if self._stack:
            self._cwd, self._cursor, self._scroll = self._stack.pop()
            self._load_dir()
        else:
            self.on_exit()

    def update(self):
        pass

    # ── Dosya Sistemi ─────────────────────────────────────────
    def _load_dir(self):
        self._entries = []
        try:
            items = sorted(os.listdir(self._cwd))
        except PermissionError:
            self.notify("Izin reddedildi!")
            if self._stack:
                self._cwd, self._cursor, self._scroll = self._stack.pop()
                self._load_dir()
            else:
                self._cwd = START_DIR
                self._load_dir()
            return

        # Üst dizin girişi
        if self._cwd != "/":
            self._entries.append(FileEntry("..", self._cwd, True, 0))

        for name in items:
            full = os.path.join(self._cwd, name)
            try:
                st     = os.stat(full)
                is_dir = stat.S_ISDIR(st.st_mode)
                size   = st.st_size
            except Exception:
                is_dir = False
                size   = 0
            self._entries.append(FileEntry(name, full, is_dir, size))

    # ── Çizim ─────────────────────────────────────────────────
    def draw(self, fb: Framebuffer):
        if self._info_mode and self._entries:
            self._draw_info(fb, self._entries[self._cursor])
            return

        # Başlık: mevcut dizin
        cwd_disp = self._cwd[-20:] if len(self._cwd) > 20 else self._cwd
        fb.icon("folder", 1, CONTENT_Y)
        fb.text(cwd_disp, 12, CONTENT_Y)
        fb.hline(0, CONTENT_Y + 9, 128)

        y         = CONTENT_Y + 11
        max_lines = (55 - y) // LINE_H

        visible = self._entries[self._scroll: self._scroll + max_lines]
        for idx, entry in enumerate(visible):
            abs_idx  = self._scroll + idx
            selected = (abs_idx == self._cursor)

            if selected:
                fb.rect(0, y - 1, 128, LINE_H + 1, fill=True)

            # İkon
            ico = "folder" if entry.is_dir else "terminal"
            # Sadece sembol kullan (8px çok geniş; küçük prefix)
            prefix = "/" if entry.is_dir else " "

            # İsim (max 17 karakter) + boyut (sağda)
            name = (prefix + entry.name)[:17]
            fb.text(name, 1, y, on=not selected)

            if not entry.is_dir and entry.name != "..":
                sz = entry.size_str
                fb.text(sz, 128 - Font.text_width(sz) - 1, y, on=not selected)

            y += LINE_H

        # Scrollbar
        if len(self._entries) > max_lines:
            sb_h  = max(2, max_lines * max_lines // len(self._entries))
            sb_y  = CONTENT_Y + 11 + self._scroll * (max_lines * LINE_H) // len(self._entries)
            fb.vline(127, sb_y, sb_h)

        # İpucu
        fb.text("SEL:ac LONG:geri", 1, 56)

    def _draw_info(self, fb: Framebuffer, entry: FileEntry):
        fb.text("Dosya Bilgisi", 1, CONTENT_Y)
        fb.hline(0, CONTENT_Y + 9, 128)
        y = CONTENT_Y + 12

        fb.text(entry.name[:21],    1, y); y += LINE_H
        fb.text(f"Yol: {entry.path[-20:]}", 1, y); y += LINE_H
        tipe = "Dizin" if entry.is_dir else "Dosya"
        fb.text(f"Tur: {tipe}", 1, y); y += LINE_H
        if not entry.is_dir:
            fb.text(f"Boy: {entry.size_str}", 1, y); y += LINE_H

        fb.text("SEL/LONG: geri", 1, 56)
