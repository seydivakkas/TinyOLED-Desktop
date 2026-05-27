/**
 * TinyOLED Desktop — App Launcher (JavaScript Port)
 * 3×2 icon grid with paged navigation and selection animation.
 */

import { Font } from './font.js';

const CONTENT_Y = 10;
const CONTENT_H = 44;
const COLS = 3;
const ROWS = 2;
const CELL_W = Math.floor(128 / COLS);  // ~42
const CELL_H = Math.floor(CONTENT_H / ROWS);  // ~22

export class Launcher {
  constructor() {
    this._apps = [];
    this._cursor = 0;
    this._animOffset = 0;
  }

  register(name, label, icon, callback) {
    this._apps.push({ name, label, icon, callback });
  }

  moveUp() {
    if (this._cursor > 0) {
      this._cursor--;
      this._animOffset = 3;
    }
  }

  moveDown() {
    if (this._cursor < this._apps.length - 1) {
      this._cursor++;
      this._animOffset = -3;
    }
  }

  select() {
    if (this._cursor >= 0 && this._cursor < this._apps.length) {
      this._apps[this._cursor].callback();
    }
  }

  currentApp() {
    return this._apps[this._cursor] || null;
  }

  get appCount() {
    return this._apps.length;
  }

  draw(fb) {
    const perPage = COLS * ROWS;
    const visibleStart = Math.floor(this._cursor / perPage) * perPage;
    const visibleApps = this._apps.slice(visibleStart, visibleStart + perPage);

    for (let idx = 0; idx < visibleApps.length; idx++) {
      const app = visibleApps[idx];
      const col = idx % COLS;
      const row = Math.floor(idx / COLS);
      const cx = col * CELL_W;
      const cy = CONTENT_Y + row * CELL_H;
      const absIdx = visibleStart + idx;
      const selected = (absIdx === this._cursor);

      // Selected cell background
      if (selected) {
        const yOff = this._animOffset;
        fb.roundedRect(cx + 1, cy + yOff, CELL_W - 2, CELL_H - 2, 2, true, true);
      }

      // Icon (centered in cell, 8×8)
      const iconX = cx + Math.floor((CELL_W - 8) / 2);
      const iconY = cy + 2;
      fb.icon(app.icon, iconX, iconY, !selected);

      // Label (below icon)
      const label = app.label.slice(0, 5);
      const lw = Font.textWidth(label);
      const lx = cx + Math.floor((CELL_W - lw) / 2);
      fb.text(label, lx, iconY + 9, !selected);
    }

    // Decay animation
    if (this._animOffset > 0) this._animOffset--;
    else if (this._animOffset < 0) this._animOffset++;

    // Page indicators
    const totalPages = Math.ceil(this._apps.length / perPage);
    const curPage = Math.floor(this._cursor / perPage);
    if (totalPages > 1) {
      for (let p = 0; p < totalPages; p++) {
        const px = Math.floor(128 / 2) - totalPages * 3 + p * 6;
        if (p === curPage) {
          fb.rect(px, CONTENT_Y + CONTENT_H + 1, 4, 2, true, true);
        } else {
          fb.rect(px, CONTENT_Y + CONTENT_H + 1, 4, 2);
        }
      }
    }
  }
}
