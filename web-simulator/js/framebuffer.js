/**
 * TinyOLED Desktop — Software Framebuffer + 2D Renderer (JavaScript Port)
 * Provides drawing primitives on top of a 128×64 pixel buffer.
 *
 * Coordinate system: (0, 0) = top-left, x grows right, y grows down.
 * Buffer layout matches SSD1306 page format: pixel (x, y) lives in
 * byte [page * W + x], bit (y % 8).
 */

import { Font } from './font.js';

const W = 128;
const H = 64;

export class Framebuffer {
  constructor() {
    this.width = W;
    this.height = H;
    this.pages = H >> 3;
    this._buf = new Uint8Array(W * (H >> 3));
  }

  // ── Raw Pixel ──────────────────────────────────────────────
  pixel(x, y, on = true) {
    if (x >= 0 && x < W && y >= 0 && y < H) {
      const idx = (y >> 3) * W + x;
      const bit = y & 7;
      if (on) this._buf[idx] |= (1 << bit);
      else    this._buf[idx] &= ~(1 << bit);
    }
  }

  getPixel(x, y) {
    if (x >= 0 && x < W && y >= 0 && y < H) {
      return !!(this._buf[(y >> 3) * W + x] & (1 << (y & 7)));
    }
    return false;
  }

  // ── Primitives ─────────────────────────────────────────────
  clear(on = false) {
    this._buf.fill(on ? 0xFF : 0x00);
  }

  hline(x, y, w, on = true) {
    for (let i = 0; i < w; i++) this.pixel(x + i, y, on);
  }

  vline(x, y, h, on = true) {
    for (let i = 0; i < h; i++) this.pixel(x, y + i, on);
  }

  line(x0, y0, x1, y1, on = true) {
    let dx = Math.abs(x1 - x0);
    let dy = Math.abs(y1 - y0);
    const sx = x0 < x1 ? 1 : -1;
    const sy = y0 < y1 ? 1 : -1;
    let err = dx - dy;
    while (true) {
      this.pixel(x0, y0, on);
      if (x0 === x1 && y0 === y1) break;
      const e2 = 2 * err;
      if (e2 > -dy) { err -= dy; x0 += sx; }
      if (e2 < dx)  { err += dx; y0 += sy; }
    }
  }

  rect(x, y, w, h, on = true, fill = false) {
    if (fill) {
      for (let row = 0; row < h; row++) this.hline(x, y + row, w, on);
    } else {
      this.hline(x,         y,         w, on);
      this.hline(x,         y + h - 1, w, on);
      this.vline(x,         y,         h, on);
      this.vline(x + w - 1, y,         h, on);
    }
  }

  circle(cx, cy, r, on = true, fill = false) {
    let x = r, y = 0, err = 0;
    while (x >= y) {
      if (fill) {
        this.hline(cx - x, cy + y, 2 * x + 1, on);
        this.hline(cx - x, cy - y, 2 * x + 1, on);
        this.hline(cx - y, cy + x, 2 * y + 1, on);
        this.hline(cx - y, cy - x, 2 * y + 1, on);
      }
      const points = [
        [cx + x, cy + y], [cx - x, cy + y],
        [cx + x, cy - y], [cx - x, cy - y],
        [cx + y, cy + x], [cx - y, cy + x],
        [cx + y, cy - x], [cx - y, cy - x],
      ];
      for (const [px, py] of points) this.pixel(px, py, on);
      y++;
      err += 2 * y + 1;
      if (2 * (err - x) + 1 > 0) { x--; err += 1 - 2 * x; }
    }
  }

  roundedRect(x, y, w, h, r, on = true, fill = false) {
    if (fill) {
      this.rect(x + r, y, w - 2 * r, h, on, true);
      this.rect(x, y + r, r, h - 2 * r, on, true);
      this.rect(x + w - r, y + r, r, h - 2 * r, on, true);
    } else {
      this.hline(x + r, y,         w - 2 * r, on);
      this.hline(x + r, y + h - 1, w - 2 * r, on);
      this.vline(x,         y + r, h - 2 * r, on);
      this.vline(x + w - 1, y + r, h - 2 * r, on);
    }
    for (let dx = 0; dx < r; dx++) {
      const dy = Math.round(Math.sqrt(r * r - dx * dx));
      if (fill) {
        this.vline(x + r - dx - 1, y + r - dy,     dy, on);
        this.vline(x + w - r + dx, y + r - dy,     dy, on);
        this.vline(x + r - dx - 1, y + h - r,      dy, on);
        this.vline(x + w - r + dx, y + h - r,      dy, on);
      } else {
        this.pixel(x + r - dx - 1, y + r - dy,     on);
        this.pixel(x + w - r + dx, y + r - dy,     on);
        this.pixel(x + r - dx - 1, y + h - r + dy - 1, on);
        this.pixel(x + w - r + dx, y + h - r + dy - 1, on);
      }
    }
  }

  // ── Text & Icons ───────────────────────────────────────────
  text(s, x, y, on = true, invert = false) {
    let cx = x;
    for (const char of s) {
      const cols = Font.glyph(char);
      for (let ci = 0; ci < cols.length; ci++) {
        for (let ri = 0; ri < Font.CHAR_H; ri++) {
          let pxOn = !!(cols[ci] & (1 << ri));
          if (invert) pxOn = !pxOn;
          this.pixel(cx + ci, y + ri, on ? pxOn : !pxOn);
        }
      }
      cx += Font.CHAR_STRIDE;
    }
  }

  textCentered(s, y, on = true) {
    const tw = Font.textWidth(s);
    const x = Math.max(0, Math.floor((W - tw) / 2));
    this.text(s, x, y, on);
  }

  icon(name, x, y, on = true) {
    const rows = Font.icon(name);
    for (let ri = 0; ri < rows.length; ri++) {
      for (let bit = 0; bit < 8; bit++) {
        const pxOn = !!(rows[ri] & (0x80 >> bit));
        this.pixel(x + bit, y + ri, on ? pxOn : !pxOn);
      }
    }
  }

  progressBar(x, y, w, h, value, maxVal = 100) {
    this.rect(x, y, w, h);
    const fillW = Math.floor((w - 2) * Math.min(value, maxVal) / maxVal);
    if (fillW > 0) this.rect(x + 1, y + 1, fillW, h - 2, true, true);
  }

  invertRegion(x, y, w, h) {
    for (let row = 0; row < h; row++) {
      for (let col = 0; col < w; col++) {
        const px = this.getPixel(x + col, y + row);
        this.pixel(x + col, y + row, !px);
      }
    }
  }

  // ── Buffer Management ──────────────────────────────────────
  getBuffer() {
    return new Uint8Array(this._buf);
  }
}
