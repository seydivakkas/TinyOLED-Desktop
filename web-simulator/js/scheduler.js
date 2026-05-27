/**
 * TinyOLED Desktop — Cooperative Task Scheduler (JavaScript Port)
 * Runs periodic tasks within the requestAnimationFrame loop.
 */

export class Scheduler {
  constructor() {
    this._tasks = new Map();
  }

  add(name, fn, interval) {
    this._tasks.set(name, {
      name,
      fn,
      interval,          // seconds
      lastRun: 0,
      enabled: true,
    });
  }

  remove(name) {
    this._tasks.delete(name);
  }

  enable(name, state = true) {
    const t = this._tasks.get(name);
    if (t) t.enabled = state;
  }

  tick() {
    const now = performance.now() / 1000;
    for (const task of this._tasks.values()) {
      if (task.enabled && (now - task.lastRun) >= task.interval) {
        try { task.fn(); } catch (e) {
          console.error(`[SCHED] '${task.name}' error:`, e);
        }
        task.lastRun = now;
      }
    }
  }
}
