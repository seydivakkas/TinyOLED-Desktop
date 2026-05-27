/**
 * TinyOLED Desktop — Status Bar (JavaScript Port)
 * 128 × 9 piksel şerit — en üstte her zaman görünür.
 * Simüle edilmiş verilerle: saat, CPU, sıcaklık, WiFi
 */

import { Font } from './font.js';

const BAR_H = 9;

export class StatusBar {
  constructor() {
    this.timeStr  = '00:00';
    this.cpuPct   = 0;
    this.tempC    = 0;
    this.wifiOk   = true;
    this._tick    = 0;
  }

  update() {
    // Real time
    const now = new Date();
    this.timeStr = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;

    // Simulated CPU (oscillating 15-65%)
    this._tick++;
    this.cpuPct = Math.floor(40 + 25 * Math.sin(this._tick * 0.1));

    // Simulated temp (38-52°C)
    this.tempC = Math.floor(45 + 7 * Math.sin(this._tick * 0.05));

    this.wifiOk = true;
  }

  draw(fb) {
    // Bottom separator line
    fb.hline(0, BAR_H - 1, 128, true);

    // Left: time
    fb.text(this.timeStr, 1, 1);

    // Right side (right-to-left)
    let x = 126;

    // Temperature
    const tempStr = `${this.tempC}C`;
    x -= Font.textWidth(tempStr);
    fb.text(tempStr, x, 1);
    x -= 2;

    // CPU
    const cpuStr = `${this.cpuPct}%`;
    x -= Font.textWidth(cpuStr);
    fb.text(cpuStr, x, 1);
    x -= 3;

    // WiFi icon
    x -= 8;
    if (this.wifiOk) {
      fb.icon('wifi', x, 0);
    } else {
      fb.icon('wifi', x, 0);
      fb.line(x, 0, x + 7, 7);
    }
  }
}
