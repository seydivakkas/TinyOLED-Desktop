/**
 * TinyOLED Desktop — browser application runtime.
 * Shared UI/state helpers for the 42 browser-native / bridge-aware ports.
 */
export const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

export function loadJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

export function saveJSON(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch {}
}

export function short(value, max = 11) {
  const s = String(value ?? '--');
  return s.length <= max ? s : `${s.slice(0, Math.max(1, max - 1))}~`;
}

export class BrowserApp {
  constructor(onExit, { title, mode = 'WEB', items = [] } = {}) {
    this.onExit = onExit;
    this.title = title || 'App';
    this.mode = mode;
    this.items = items;
    this.cursor = 0;
    this.status = 'hazir';
    this.busy = false;
    this.lastError = '';
    this._tick = 0;
  }

  onUp() {
    if (!this.items.length) return;
    this.cursor = (this.cursor - 1 + this.items.length) % this.items.length;
  }

  onDown() {
    if (!this.items.length) return;
    this.cursor = (this.cursor + 1) % this.items.length;
  }

  onLong() { this.onExit(); }
  update() { this._tick++; }

  selected() {
    return this.items[this.cursor] ?? null;
  }

  setItems(items) {
    this.items = items || [];
    if (this.cursor >= this.items.length) this.cursor = Math.max(0, this.items.length - 1);
  }

  async task(fn, label = 'calisiyor') {
    if (this.busy) return;
    this.busy = true;
    this.status = label;
    this.lastError = '';
    try {
      await fn();
      if (this.status === label) this.status = 'tamam';
    } catch (err) {
      console.error(err);
      this.lastError = err?.message || String(err);
      this.status = 'hata';
    } finally {
      this.busy = false;
    }
  }

  drawHeader(fb, mode = this.mode) {
    fb.text(short(mode, 5), 1, 11);
    fb.text(short(this.title, 13), 31, 11);
    fb.hline(1, 19, 126);
  }

  drawRows(fb, rows, selectedIndex = -1, y0 = 22) {
    const visible = rows.slice(0, 4);
    for (let i = 0; i < visible.length; i++) {
      const [label, value] = visible[i];
      const selected = i === selectedIndex;
      const y = y0 + i * 8;
      if (selected) fb.rect(0, y - 1, 128, 8, true, true);
      fb.text(short(`${label}:`, 9), 2, y, !selected);
      const txt = short(value, 11);
      fb.text(txt, Math.max(58, 126 - txt.length * 6), y, !selected);
    }
  }

  footer(fb, text = this.status) {
    const pulse = (this._tick >> 3) & 1;
    fb.text(short(`${pulse ? '>' : ' '} ${text}`, 20), 1, 56);
  }

  draw(fb) {
    this.drawHeader(fb);
    const rows = this.items.map((item, idx) => [
      item.label ?? `#${idx + 1}`,
      item.value ?? item.state ?? ''
    ]);
    this.drawRows(fb, rows, this.cursor);
    this.footer(fb);
  }
}

export function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export async function pickFile(accept = '*/*') {
  if ('showOpenFilePicker' in window) {
    const [handle] = await window.showOpenFilePicker({
      multiple: false,
      types: [{ description: 'Dosya', accept: { [accept.startsWith('audio') ? 'audio/*' : accept.startsWith('video') ? 'video/*' : 'application/octet-stream']: ['.*'] } }]
    }).catch(async () => {
      const [handle] = await window.showOpenFilePicker({ multiple: false });
      return [handle];
    });
    return handle.getFile();
  }

  return await new Promise((resolve, reject) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = accept;
    input.onchange = () => input.files?.[0] ? resolve(input.files[0]) : reject(new Error('Dosya secilmedi'));
    input.click();
  });
}
