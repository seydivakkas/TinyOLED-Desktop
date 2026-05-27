/**
 * TinyOLED Desktop — Notification System (JavaScript Port)
 * Bottom-bar notifications with countdown progress bar.
 */

import { Font } from './font.js';

const NOTIF_Y = 55;
const NOTIF_H = 9;

class Notification {
  constructor(message, duration = 2.0) {
    this.message  = message;
    this.duration = duration;
    this.created  = performance.now() / 1000;
  }

  isExpired() {
    return (performance.now() / 1000 - this.created) >= this.duration;
  }

  progress() {
    return Math.min(1.0, (performance.now() / 1000 - this.created) / this.duration);
  }
}

export class NotificationManager {
  constructor() {
    this._current = null;
    this._queue = [];
  }

  push(message, duration = 2.5) {
    const n = new Notification(message, duration);
    if (!this._current) {
      this._current = n;
    } else {
      this._queue.push(n);
    }
  }

  tick() {
    if (this._current && this._current.isExpired()) {
      this._current = this._queue.length > 0 ? this._queue.shift() : null;
    }
  }

  draw(fb) {
    if (!this._current) return;
    const n = this._current;

    // Solid background
    fb.rect(0, NOTIF_Y, 128, NOTIF_H, true, true);

    // Centered text (inverted)
    const maxChars = Math.floor(128 / Font.CHAR_STRIDE);
    const msg = n.message.slice(0, maxChars);
    const tw = Font.textWidth(msg);
    const x = Math.max(1, Math.floor((128 - tw) / 2));
    fb.text(msg, x, NOTIF_Y + 1, false);

    // Progress bar
    const barW = Math.floor(126 * (1.0 - n.progress()));
    if (barW > 0) fb.hline(1, NOTIF_Y + NOTIF_H - 1, barW, false);
  }

  get active() {
    return this._current !== null;
  }
}
