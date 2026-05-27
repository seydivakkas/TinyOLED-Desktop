/** TinyOLED Desktop — Clock App (Analog + Digital) */
import { Font } from '../font.js';

const CONTENT_Y = 10;
const CX = 64, CY = 35, R = 22;

export class ClockApp {
  static NAME = 'clock'; static LABEL = 'Saat'; static ICON = 'clock';
  constructor(onExit) { this.onExit = onExit; this.mode = 'digital'; this._tick = 0; }
  onUp()   { this.mode = this.mode === 'digital' ? 'analog' : 'digital'; }
  onDown() {}
  onSel()  { this.onExit(); }
  onLong() { this.onExit(); }
  update() { this._tick++; }

  draw(fb) {
    const now = new Date();
    this.mode === 'digital' ? this._digital(fb, now) : this._analog(fb, now);
  }

  _bigText(fb, text, x, y, scale = 2) {
    let cx = x;
    for (const ch of text) {
      const cols = Font.glyph(ch);
      for (let ci = 0; ci < cols.length; ci++) {
        for (let ri = 0; ri < Font.CHAR_H; ri++) {
          if (cols[ci] & (1 << ri))
            fb.rect(cx + ci * scale, y + ri * scale, scale, scale, true, true);
        }
      }
      cx += (Font.CHAR_W + Font.CHAR_SPACING) * scale;
    }
  }

  _digital(fb, t) {
    const h = String(t.getHours()).padStart(2, '0');
    const m = String(t.getMinutes()).padStart(2, '0');
    const s = String(t.getSeconds()).padStart(2, '0');
    this._bigText(fb, h, 4, CONTENT_Y + 4, 3);
    this._bigText(fb, ':', 4 + 2 * 6 * 3 + 1, CONTENT_Y + 4, 3);
    this._bigText(fb, m, 4 + 2 * 6 * 3 + 6, CONTENT_Y + 4, 3);
    fb.text(`:${s}`, 110, CONTENT_Y + 20);
    const days = ['Pzt','Sal','Car','Per','Cum','Cmt','Paz'];
    const months = ['Oca','Sub','Mar','Nis','May','Haz','Tem','Agu','Eyl','Eki','Kas','Ara'];
    const d = days[t.getDay() === 0 ? 6 : t.getDay() - 1];
    const mn = months[t.getMonth()];
    fb.textCentered(`${d} ${t.getDate()} ${mn} ${t.getFullYear()}`, CONTENT_Y + 36);
    fb.text('[UP]mod', 1, 56);
  }

  _analog(fb, t) {
    const cx = CX, cy = CY, r = R;
    fb.circle(cx, cy, r);
    for (let i = 0; i < 12; i++) {
      const a = (i * 30 - 90) * Math.PI / 180;
      fb.line(
        Math.round(cx + (r-3)*Math.cos(a)), Math.round(cy + (r-3)*Math.sin(a)),
        Math.round(cx + (r-1)*Math.cos(a)), Math.round(cy + (r-1)*Math.sin(a))
      );
    }
    // Minute hand
    const ma = (t.getMinutes() * 6 - 90) * Math.PI / 180;
    fb.line(cx, cy, Math.round(cx+(r-5)*Math.cos(ma)), Math.round(cy+(r-5)*Math.sin(ma)));
    // Hour hand
    const ha = ((t.getHours()%12)*30 + t.getMinutes()*0.5 - 90) * Math.PI / 180;
    const hx = Math.round(cx+(r-10)*Math.cos(ha)), hy = Math.round(cy+(r-10)*Math.sin(ha));
    fb.line(cx, cy, hx, hy);
    fb.line(cx+1, cy, hx+1, hy);
    // Second hand (dotted)
    const sa = (t.getSeconds() * 6 - 90) * Math.PI / 180;
    for (let step = 0; step < r-3; step += 2)
      fb.pixel(Math.round(cx+step*Math.cos(sa)), Math.round(cy+step*Math.sin(sa)));
    fb.circle(cx, cy, 2, true, true);
    // Digital sidebar
    fb.text(`${String(t.getHours()).padStart(2,'0')}:${String(t.getMinutes()).padStart(2,'0')}`, 96, CONTENT_Y+4);
    fb.text(`:${String(t.getSeconds()).padStart(2,'0')}`, 96, CONTENT_Y+14);
    fb.text(`${t.getDate()}/${t.getMonth()+1}`, 96, CONTENT_Y+28);
    fb.text(String(t.getFullYear()), 96, CONTENT_Y+38);
    fb.text('[UP]mod', 1, 56);
  }
}
