/**
 * TinyOLED Desktop — shared browser port base
 *
 * PORT   = browser-native implementation/simulation
 * MOCK   = deterministic demo data; no private credentials or remote side effects
 * BRIDGE = UI/state port for features that need Raspberry Pi/Linux/hardware for real I/O
 */
export class CatalogApp {
  constructor(onExit, spec) {
    this.onExit = onExit;
    this.spec = spec;
    this.cursor = 0;
    this.actionCount = 0;
    this.tick = 0;
  }

  onUp() {
    const n = this.spec.rows.length;
    this.cursor = (this.cursor - 1 + n) % n;
  }

  onDown() {
    const n = this.spec.rows.length;
    this.cursor = (this.cursor + 1) % n;
  }

  onSel() {
    this.actionCount = (this.actionCount + 1) % 100;
  }

  onLong() { this.onExit(); }
  update() { this.tick++; }

  draw(fb) {
    const mode = this.spec.mode || 'PORT';
    const modeLabel = mode === 'BRIDGE' ? 'BRG' : mode;
    fb.text(modeLabel, 1, 11);
    fb.text(this.spec.title.slice(0, 12), 31, 11);
    fb.hline(1, 19, 126);

    const rows = this.spec.rows;
    const y0 = 22;
    for (let i = 0; i < Math.min(rows.length, 4); i++) {
      const [label, rawValue] = rows[i];
      const selected = i === this.cursor;
      const y = y0 + i * 8;
      let value = rawValue;
      if (selected && this.actionCount > 0) value = `${rawValue}`.slice(0, 10);

      if (selected) fb.rect(0, y - 1, 128, 8, true, true);
      fb.text(`${label}:`.slice(0, 9), 2, y, !selected);
      const valueText = `${value}`.slice(0, 11);
      fb.text(valueText, Math.max(58, 126 - valueText.length * 6), y, !selected);
    }

    const pulse = (this.tick >> 3) & 1;
    const action = this.spec.action || 'SEL';
    fb.text(`${pulse ? '>' : ' '} ${action}`.slice(0, 20), 1, 56);
  }
}
