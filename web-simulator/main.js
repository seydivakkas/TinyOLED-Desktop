/**
 * TinyOLED Desktop — Web Simulator Entry Point
 */
import { Desktop } from './js/shell.js';

document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('oled-canvas');
  if (!canvas) { console.error('Canvas element not found'); return; }

  const desktop = new Desktop(canvas);

  // Info panel updates
  const stateEl = document.getElementById('info-state');
  const appEl   = document.getElementById('info-app');

  desktop.onStateChange = (state, appName) => {
    if (stateEl) stateEl.textContent = state;
    if (appEl)   appEl.textContent = appName;
  };

  desktop.run();
  console.log('TinyOLED Desktop Simulator started.');
});
