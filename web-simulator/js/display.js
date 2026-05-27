/**
 * TinyOLED Desktop — Canvas OLED Display Renderer
 * Renders the 128×64 framebuffer onto an HTML Canvas with
 * realistic OLED pixel aesthetics (glow, gaps, color).
 */

const OLED_W = 128;
const OLED_H = 64;

export class OLEDDisplay {
  /**
   * @param {HTMLCanvasElement} canvas
   * @param {Object} opts
   * @param {number} opts.pixelSize - CSS pixels per OLED pixel (default 5)
   * @param {number} opts.gap - Gap between pixels (default 1)
   * @param {string} opts.onColor - Active pixel color
   * @param {string} opts.offColor - Inactive pixel color
   */
  constructor(canvas, opts = {}) {
    this.canvas = canvas;
    this.pixelSize = opts.pixelSize || 5;
    this.gap = opts.gap || 1;
    this.onColor = opts.onColor || '#00e5ff';
    this.offColor = opts.offColor || '#0a0e14';
    this.glowColor = opts.glowColor || 'rgba(0, 229, 255, 0.15)';

    // Size the canvas
    this.canvas.width = OLED_W * this.pixelSize;
    this.canvas.height = OLED_H * this.pixelSize;
    this.ctx = this.canvas.getContext('2d');

    // Pre-fill with off
    this.ctx.fillStyle = this.offColor;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
  }

  /**
   * Render a Framebuffer onto the canvas.
   * @param {import('./framebuffer.js').Framebuffer} fb
   */
  render(fb) {
    const ctx = this.ctx;
    const ps = this.pixelSize;
    const g = this.gap;
    const buf = fb.getBuffer();

    // Clear
    ctx.fillStyle = this.offColor;
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw active pixels
    ctx.fillStyle = this.onColor;
    for (let y = 0; y < OLED_H; y++) {
      const page = y >> 3;
      const bit = y & 7;
      for (let x = 0; x < OLED_W; x++) {
        if (buf[page * OLED_W + x] & (1 << bit)) {
          ctx.fillRect(
            x * ps + g,
            y * ps + g,
            ps - g * 2,
            ps - g * 2
          );
        }
      }
    }

    // Glow pass (subtle bloom)
    ctx.globalCompositeOperation = 'lighter';
    ctx.fillStyle = this.glowColor;
    for (let y = 0; y < OLED_H; y++) {
      const page = y >> 3;
      const bit = y & 7;
      for (let x = 0; x < OLED_W; x++) {
        if (buf[page * OLED_W + x] & (1 << bit)) {
          ctx.fillRect(
            x * ps - 1,
            y * ps - 1,
            ps + 2,
            ps + 2
          );
        }
      }
    }
    ctx.globalCompositeOperation = 'source-over';
  }
}
