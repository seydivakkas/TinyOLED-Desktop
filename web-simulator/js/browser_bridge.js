/**
 * TinyOLED Desktop — local bridge + Web Serial helpers.
 * No credential is committed. Bridge base URL is stored only in this browser.
 */
const BRIDGE_KEY = 'tinyoled.bridge.base';
let serialPort = null;

export function bridgeBase() {
  return localStorage.getItem(BRIDGE_KEY) || '';
}

export function configureBridge(force = false) {
  const existing = bridgeBase();
  if (existing && !force) return existing;
  const current = existing || 'http://127.0.0.1:8765';
  const next = prompt('TinyOLED bridge URL', current);
  if (next) {
    localStorage.setItem(BRIDGE_KEY, next.replace(/\/+$/, ''));
    return next.replace(/\/+$/, '');
  }
  return existing;
}

export async function bridgeJSON(path, options = {}) {
  const base = bridgeBase() || configureBridge();
  if (!base) throw new Error('Bridge URL ayarlanmadi');
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), options.timeout || 3500);
  try {
    const res = await fetch(`${base}${path}`, {
      method: options.method || 'GET',
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
      body: options.body === undefined ? undefined : JSON.stringify(options.body),
      signal: controller.signal
    });
    if (!res.ok) throw new Error(`Bridge HTTP ${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}

export function serialSupported() {
  return 'serial' in navigator;
}

async function ensureSerial(baudRate = 115200) {
  if (!serialSupported()) throw new Error('Web Serial desteklenmiyor');
  if (!serialPort) serialPort = await navigator.serial.requestPort();
  if (!serialPort.readable || !serialPort.writable) {
    await serialPort.open({ baudRate });
  }
  return serialPort;
}

export async function serialExchange(command, { baudRate = 115200, timeout = 2000 } = {}) {
  const port = await ensureSerial(baudRate);
  const writer = port.writable.getWriter();
  try {
    await writer.write(new TextEncoder().encode(`${JSON.stringify(command)}\n`));
  } finally {
    writer.releaseLock();
  }

  const reader = port.readable.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  const deadline = Date.now() + timeout;
  try {
    while (Date.now() < deadline) {
      const remaining = Math.max(1, deadline - Date.now());
      let result;
      try {
        result = await Promise.race([
          reader.read(),
          new Promise((_, reject) => setTimeout(() => reject(new Error('Serial timeout')), remaining))
        ]);
      } catch (err) {
        try { await reader.cancel(); } catch {}
        throw err;
      }
      if (result.done) break;
      buffer += decoder.decode(result.value, { stream: true });
      const nl = buffer.indexOf('\n');
      if (nl >= 0) {
        const line = buffer.slice(0, nl).trim();
        return line ? JSON.parse(line) : {};
      }
    }
    throw new Error('Serial cevap yok');
  } finally {
    try { reader.releaseLock(); } catch {}
  }
}

export async function ioCommand(command, bridgePath = '/api/io') {
  if (bridgeBase()) {
    return bridgeJSON(bridgePath, { method: 'POST', body: command });
  }
  if (serialSupported()) {
    try { return await serialExchange(command); } catch (err) { console.warn('Serial fallback:', err); }
  }
  return bridgeJSON(bridgePath, { method: 'POST', body: command });
}
