/**
 * TinyOLED Desktop — Desktop Shell (JavaScript Port)
 * State machine: SPLASH → HOME → APP
 * Combines StatusBar + Launcher + Notification + Apps
 */

import { Framebuffer }        from './framebuffer.js';
import { OLEDDisplay }        from './display.js';
import { InputManager, EVT_UP, EVT_DOWN, EVT_SEL, EVT_LONG } from './input.js';
import { Scheduler }          from './scheduler.js';
import { StatusBar }          from './statusbar.js';
import { Launcher }           from './launcher.js';
import { NotificationManager } from './notification.js';

import { ClockApp }      from './apps/clock.js';
import { SysInfoApp }    from './apps/sysinfo.js';
import { SnakeApp }      from './apps/snake.js';
import { FlappyApp }     from './apps/flappy.js';
import { DiceApp }       from './apps/dice.js';
import { Cube3DApp }     from './apps/cube3d.js';
import { FractalApp }    from './apps/fractal.js';
import { BreathingApp }  from './apps/breathing.js';
import { MoonApp }       from './apps/moon.js';
import { PomodoroApp }   from './apps/pomodoro.js';
import { StarfieldApp }  from './apps/starfield.js';
import { MatrixRainApp } from './apps/matrix.js';
import { GameOfLifeApp } from './apps/gameoflife.js';
import { DVDLogoApp }    from './apps/dvd.js';
import { SettingsApp }   from './apps/settings.js';

const State = { SPLASH: 0, HOME: 1, APP: 2 };
const SPLASH_FRAMES = 40;
const TARGET_FPS = 20;

export class Desktop {
  constructor(canvas) {
    this._display  = new OLEDDisplay(canvas);
    this._fb       = new Framebuffer();
    this._state    = State.SPLASH;
    this._app      = null;
    this._splashT  = 0;

    this._statusbar = new StatusBar();
    this._launcher  = new Launcher();
    this._notif     = new NotificationManager();
    this._sched     = new Scheduler();
    this._input     = new InputManager();

    // Info panel callback
    this._onStateChange = null;

    this._registerApps();
    this._registerTasks();
    this._bindButtons();
  }

  set onStateChange(fn) { this._onStateChange = fn; }

  _registerApps() {
    const ex = () => this._goHome();
    const nx = (msg, dur) => this._notif.push(msg, dur);

    // Sistem
    this._launcher.register('clock',   'Saat',   'clock',   () => this._open(new ClockApp(ex)));
    this._launcher.register('sysinfo', 'Sistem', 'cpu',     () => this._open(new SysInfoApp(ex)));
    // Oyunlar
    this._launcher.register('snake',   'Yilan',  'snake',   () => this._open(new SnakeApp(ex)));
    this._launcher.register('flappy',  'Flappy', 'bird',    () => this._open(new FlappyApp(ex)));
    this._launcher.register('dice',    'Zar',    'dice',    () => this._open(new DiceApp(ex)));
    // 3D & Fraktal
    this._launcher.register('cube3d',  '3D',     'cube',    () => this._open(new Cube3DApp(ex)));
    this._launcher.register('fractal', 'Fraktl', 'fractal', () => this._open(new FractalApp(ex)));
    // Sağlık
    this._launcher.register('breath',  'Nefes',  'breath',  () => this._open(new BreathingApp(ex)));
    this._launcher.register('pomodoro','Pomo',   'timer',   () => this._open(new PomodoroApp(ex, nx)));
    // Astronomi
    this._launcher.register('moon',    'Ay',     'moon',    () => this._open(new MoonApp(ex)));
    // Ekran Koruyucular
    this._launcher.register('starfield','Yldiz', 'star',    () => this._open(new StarfieldApp(ex)));
    this._launcher.register('matrix',  'Matrx',  'matrix',  () => this._open(new MatrixRainApp(ex)));
    this._launcher.register('life',    'Life',   'cell',    () => this._open(new GameOfLifeApp(ex)));
    this._launcher.register('dvd',     'DVD',    'dvd',     () => this._open(new DVDLogoApp(ex)));
    // Ayarlar
    this._launcher.register('settings','Ayar',   'gear',    () => this._open(new SettingsApp(ex, nx)));
  }

  _registerTasks() {
    this._sched.add('statusbar', () => this._statusbar.update(), 1.0);
    this._sched.add('notif',     () => this._notif.tick(),       0.1);
    this._sched.add('app_update',() => this._tickApp(),          0.05);
  }

  _bindButtons() {
    this._input.on(EVT_UP,   () => this._onUp());
    this._input.on(EVT_DOWN, () => this._onDown());
    this._input.on(EVT_SEL,  () => this._onSel());
    this._input.on(EVT_LONG, () => this._onLong());
  }

  // ── State Transitions ──────────────────────────────────────
  _open(app) {
    this._app = app;
    this._state = State.APP;
    this._emitState();
  }

  _goHome() {
    this._app = null;
    this._state = State.HOME;
    this._emitState();
  }

  _emitState() {
    if (this._onStateChange) {
      const stateNames = ['SPLASH', 'HOME', 'APP'];
      const appName = this._app ? (this._app.constructor.LABEL || this._app.constructor.NAME || '?') : 'Launcher';
      this._onStateChange(stateNames[this._state], appName);
    }
  }

  // ── Button Events ──────────────────────────────────────────
  _onUp() {
    if (this._state === State.HOME) this._launcher.moveUp();
    else if (this._state === State.APP && this._app?.onUp) this._app.onUp();
  }

  _onDown() {
    if (this._state === State.HOME) this._launcher.moveDown();
    else if (this._state === State.APP && this._app?.onDown) this._app.onDown();
  }

  _onSel() {
    if (this._state === State.HOME) this._launcher.select();
    else if (this._state === State.APP && this._app?.onSel) this._app.onSel();
  }

  _onLong() {
    if (this._state === State.APP && this._app?.onLong) this._app.onLong();
    else this._goHome();
  }

  _tickApp() {
    if (this._app?.update) this._app.update();
  }

  // ── Main Loop ──────────────────────────────────────────────
  run() {
    this._input.start();
    this._notif.push('TinyOLED v1.0 hazir!', 2.0);
    this._emitState();

    const frameMs = 1000 / TARGET_FPS;
    let lastFrame = 0;

    const loop = (ts) => {
      if (ts - lastFrame >= frameMs) {
        lastFrame = ts;
        this._sched.tick();
        this._render();
      }
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  // ── Render ─────────────────────────────────────────────────
  _render() {
    const fb = this._fb;
    fb.clear();

    if (this._state === State.SPLASH) {
      this._drawSplash();
    } else if (this._state === State.HOME) {
      this._statusbar.draw(fb);
      this._launcher.draw(fb);
    } else if (this._state === State.APP && this._app) {
      this._statusbar.draw(fb);
      this._app.draw(fb);
    }

    if (this._notif.active) this._notif.draw(fb);

    this._display.render(fb);

    // Splash → HOME transition
    if (this._state === State.SPLASH) {
      this._splashT++;
      if (this._splashT >= SPLASH_FRAMES) {
        this._state = State.HOME;
        this._emitState();
      }
    }
  }

  _drawSplash() {
    const fb = this._fb;
    const t = this._splashT;

    if (t < 15) {
      fb.circle(64, 32, t * 2, true, true);
    } else {
      fb.circle(64, 32, 30, true, true);
      fb.textCentered('TinyOLED', 22, false);
      fb.textCentered('Desktop v1.0', 31, false);
      fb.textCentered('Simulator', 40, false);
    }

    if (t >= 20) {
      const progress = Math.min(1.0, (t - 20) / (SPLASH_FRAMES - 20));
      const barW = Math.floor(100 * progress);
      fb.rect(14, 56, 100, 5);
      if (barW > 0) fb.rect(15, 57, barW - 1, 3, true, true);
    }
  }
}
