"""
TinyOLED Desktop — Software Framebuffer + 2D Renderer
Provides drawing primitives on top of the raw SSD1306 pixel buffer.

Coordinate system: (0, 0) = top-left, x grows right, y grows down.
All draw calls write into a bytearray identical to SSD1306's page format,
then flush to hardware via SSD1306.blit() + SSD1306.show().
"""

import math
from typing import Optional, Tuple, List

from core.display import SSD1306, DISPLAY_WIDTH, DISPLAY_HEIGHT
from core.font import Font


W = DISPLAY_WIDTH    # 128
H = DISPLAY_HEIGHT   # 64


class Framebuffer:
    """
    Software framebuffer matching SSD1306 page layout.
    Pixel (x, y) lives in byte [page * W + x], bit (y % 8).
    """

    def __init__(self):
        self.width  = W
        self.height = H
        self.pages  = H // 8
        self._buf   = bytearray(W * (H // 8))

    # ── Raw Pixel ─────────────────────────────────────────────
    def pixel(self, x: int, y: int, on: bool = True):
        if 0 <= x < W and 0 <= y < H:
            idx = (y // 8) * W + x
            bit = y % 8
            if on:
                self._buf[idx] |= (1 << bit)
            else:
                self._buf[idx] &= ~(1 << bit)

    def get_pixel(self, x: int, y: int) -> bool:
        if 0 <= x < W and 0 <= y < H:
            return bool(self._buf[(y // 8) * W + x] & (1 << (y % 8)))
        return False

    # ── Primitives ────────────────────────────────────────────
    def clear(self, on: bool = False):
        fill = 0xFF if on else 0x00
        for i in range(len(self._buf)):
            self._buf[i] = fill

    def hline(self, x: int, y: int, w: int, on: bool = True):
        for i in range(w):
            self.pixel(x + i, y, on)

    def vline(self, x: int, y: int, h: int, on: bool = True):
        for i in range(h):
            self.pixel(x, y + i, on)

    def line(self, x0: int, y0: int, x1: int, y1: int, on: bool = True):
        """Bresenham line algorithm."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.pixel(x0, y0, on)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0  += sx
            if e2 < dx:
                err += dx
                y0  += sy

    def rect(self, x: int, y: int, w: int, h: int, on: bool = True, fill: bool = False):
        if fill:
            for row in range(h):
                self.hline(x, y + row, w, on)
        else:
            self.hline(x,         y,         w, on)
            self.hline(x,         y + h - 1, w, on)
            self.vline(x,         y,         h, on)
            self.vline(x + w - 1, y,         h, on)

    def circle(self, cx: int, cy: int, r: int, on: bool = True, fill: bool = False):
        """Midpoint circle algorithm."""
        x, y, err = r, 0, 0
        while x >= y:
            points = [
                (cx + x, cy + y), (cx - x, cy + y),
                (cx + x, cy - y), (cx - x, cy - y),
                (cx + y, cy + x), (cx - y, cy + x),
                (cx + y, cy - x), (cx - y, cy - x),
            ]
            for px, py in points:
                self.pixel(px, py, on)
            if fill:
                self.hline(cx - x, cy + y, 2 * x + 1, on)
                self.hline(cx - x, cy - y, 2 * x + 1, on)
                self.hline(cx - y, cy + x, 2 * y + 1, on)
                self.hline(cx - y, cy - x, 2 * y + 1, on)
            y  += 1
            err += 2 * y + 1
            if 2 * (err - x) + 1 > 0:
                x  -= 1
                err += 1 - 2 * x

    def rounded_rect(self, x: int, y: int, w: int, h: int, r: int,
                     on: bool = True, fill: bool = False):
        """Rectangle with rounded corners (radius r)."""
        if fill:
            self.rect(x + r, y, w - 2 * r, h, on, fill=True)
            self.rect(x, y + r, r, h - 2 * r, on, fill=True)
            self.rect(x + w - r, y + r, r, h - 2 * r, on, fill=True)
        else:
            self.hline(x + r, y,         w - 2 * r, on)
            self.hline(x + r, y + h - 1, w - 2 * r, on)
            self.vline(x,         y + r, h - 2 * r, on)
            self.vline(x + w - 1, y + r, h - 2 * r, on)

        # Corners
        for dx in range(r):
            dy = int(math.sqrt(r * r - dx * dx) + 0.5)
            if fill:
                self.vline(x + r - dx - 1, y + r - dy,     dy, on)
                self.vline(x + w - r + dx, y + r - dy,     dy, on)
                self.vline(x + r - dx - 1, y + h - r,      dy, on)
                self.vline(x + w - r + dx, y + h - r,      dy, on)
            else:
                self.pixel(x + r - dx - 1, y + r - dy,     on)
                self.pixel(x + w - r + dx, y + r - dy,     on)
                self.pixel(x + r - dx - 1, y + h - r + dy - 1, on)
                self.pixel(x + w - r + dx, y + h - r + dy - 1, on)

    # ── Text & Icons ──────────────────────────────────────────
    def text(self, s: str, x: int, y: int, on: bool = True, invert: bool = False):
        """Draw string using 5×7 font, starting at (x, y) top-left."""
        cx = x
        for char in s:
            cols = Font.glyph(char)
            for col_idx, col_byte in enumerate(cols):
                for row in range(Font.CHAR_H):
                    px_on = bool(col_byte & (1 << row))
                    if invert:
                        px_on = not px_on
                    self.pixel(cx + col_idx, y + row, px_on if on else not px_on)
            cx += Font.CHAR_STRIDE

    def text_centered(self, s: str, y: int, on: bool = True):
        """Draw text horizontally centered."""
        tw = Font.text_width(s)
        x  = max(0, (W - tw) // 2)
        self.text(s, x, y, on)

    def icon(self, name: str, x: int, y: int, on: bool = True):
        """Draw 8×8 icon at (x, y)."""
        rows = Font.icon(name)
        for row_idx, row_byte in enumerate(rows):
            for bit in range(8):
                px_on = bool(row_byte & (0x80 >> bit))
                self.pixel(x + bit, y + row_idx, px_on if on else not px_on)

    def progress_bar(self, x: int, y: int, w: int, h: int,
                     value: float, max_val: float = 100.0):
        """Draw a filled progress bar (value 0..max_val)."""
        self.rect(x, y, w, h)
        fill_w = int((w - 2) * min(value, max_val) / max_val)
        if fill_w > 0:
            self.rect(x + 1, y + 1, fill_w, h - 2, fill=True)

    def scrollable_text(self, lines: List[str], scroll: int,
                        x: int, y: int, w: int, h: int):
        """Render a scrollable list of text lines in the given bounding box."""
        max_lines = h // (Font.CHAR_H + 1)
        visible   = lines[scroll: scroll + max_lines]
        for i, line in enumerate(visible):
            # Truncate to fit width
            max_chars = w // Font.CHAR_STRIDE
            self.text(line[:max_chars], x, y + i * (Font.CHAR_H + 1))

    # ── Buffer Management ────────────────────────────────────
    def copy(self) -> bytearray:
        return bytearray(self._buf)

    def restore(self, buf: bytearray):
        length = min(len(buf), len(self._buf))
        self._buf[:length] = buf[:length]

    def flush(self, display: SSD1306):
        """Push framebuffer to physical display."""
        display.blit(self._buf)
        display.show()

    def blit_sprite(self, sprite: bytearray, sx: int, sy: int,
                    sw: int, sh: int):
        """Blit a w×h 1-bit sprite (row-packed, MSB left) at (sx, sy)."""
        byte_w = (sw + 7) // 8
        for row in range(sh):
            for col in range(sw):
                b_idx  = row * byte_w + col // 8
                b_bit  = 7 - (col % 8)
                if b_idx < len(sprite):
                    px = bool(sprite[b_idx] & (1 << b_bit))
                    self.pixel(sx + col, sy + row, px)

    def invert_region(self, x: int, y: int, w: int, h: int):
        """Invert (XOR) all pixels in a rectangular region."""
        for row in range(h):
            for col in range(w):
                px = self.get_pixel(x + col, y + row)
                self.pixel(x + col, y + row, not px)
