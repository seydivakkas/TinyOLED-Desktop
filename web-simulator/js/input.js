/**
 * TinyOLED Desktop — Input Manager (Keyboard + On-Screen Buttons)
 * Maps keyboard keys and touch/click events to UP, DOWN, SEL, LONG events.
 */

export const EVT_UP   = 'UP';
export const EVT_DOWN = 'DOWN';
export const EVT_SEL  = 'SEL';
export const EVT_LONG = 'LONG';

const LONG_PRESS_MS = 800;

export class InputManager {
  constructor() {
    this._handlers = {};
    this._pressTimers = {};
    this._started = false;
  }

  on(event, callback) {
    this._handlers[event] = callback;
  }

  emit(event) {
    const h = this._handlers[event];
    if (h) {
      try { h(); } catch (e) { console.error(`[INPUT] ${event} error:`, e); }
    }
  }

  start() {
    if (this._started) return;
    this._started = true;

    // Keyboard
    document.addEventListener('keydown', (e) => this._onKeyDown(e));
    document.addEventListener('keyup',   (e) => this._onKeyUp(e));

    // On-screen buttons
    this._bindButton('btn-up',   EVT_UP);
    this._bindButton('btn-down', EVT_DOWN);
    this._bindButton('btn-sel',  EVT_SEL);
  }

  _onKeyDown(e) {
    if (e.repeat) return;
    let evt = null;
    switch (e.key) {
      case 'w': case 'W': case 'ArrowUp':    evt = EVT_UP;   break;
      case 's': case 'S': case 'ArrowDown':  evt = EVT_DOWN; break;
      case 'Enter': case ' ':                evt = EVT_SEL;  break;
      case 'Escape':                         evt = EVT_LONG; break;
    }
    if (!evt) return;
    e.preventDefault();

    // Emit immediately
    if (evt !== EVT_LONG) {
      this.emit(evt);
      // Start long-press timer for SEL
      if (evt === EVT_SEL) {
        this._pressTimers[e.key] = setTimeout(() => {
          this.emit(EVT_LONG);
        }, LONG_PRESS_MS);
      }
    } else {
      this.emit(EVT_LONG);
    }

    // Visual feedback
    this._highlightKey(evt);
  }

  _onKeyUp(e) {
    if (this._pressTimers[e.key]) {
      clearTimeout(this._pressTimers[e.key]);
      delete this._pressTimers[e.key];
    }
  }

  _bindButton(id, evt) {
    const btn = document.getElementById(id);
    if (!btn) return;

    let longTimer = null;

    const onStart = (e) => {
      e.preventDefault();
      this.emit(evt);
      btn.classList.add('active');
      longTimer = setTimeout(() => {
        this.emit(EVT_LONG);
      }, LONG_PRESS_MS);
    };

    const onEnd = (e) => {
      e.preventDefault();
      btn.classList.remove('active');
      if (longTimer) { clearTimeout(longTimer); longTimer = null; }
    };

    // Mouse
    btn.addEventListener('mousedown',  onStart);
    btn.addEventListener('mouseup',    onEnd);
    btn.addEventListener('mouseleave', onEnd);

    // Touch
    btn.addEventListener('touchstart', onStart, { passive: false });
    btn.addEventListener('touchend',   onEnd,   { passive: false });
  }

  _highlightKey(evt) {
    const map = { UP: 'btn-up', DOWN: 'btn-down', SEL: 'btn-sel', LONG: 'btn-sel' };
    const btn = document.getElementById(map[evt]);
    if (btn) {
      btn.classList.add('active');
      setTimeout(() => btn.classList.remove('active'), 150);
    }
  }
}
