/** TinyOLED Desktop — Bouncing DVD Logo */
import { Font } from '../font.js';

export class DVDLogoApp {
  static NAME='dvd'; static LABEL='DVD'; static ICON='dvd';
  constructor(onExit) {
    this.onExit=onExit; this.x=30; this.y=20; this.dx=1.5; this.dy=1;
    this.inverted=false; this._last=0;
  }
  onUp(){} onDown(){} onSel(){} onLong(){this.onExit();}
  update() {
    const now=performance.now()/1000;
    if(now-this._last<0.04) return;
    this._last=now;
    this.x+=this.dx; this.y+=this.dy;
    const tw=Font.textWidth('TinyOLED'), th=7;
    if(this.x<=0||this.x+tw>=128){this.dx=-this.dx;this.inverted=!this.inverted;}
    if(this.y<=0||this.y+th>=64){this.dy=-this.dy;this.inverted=!this.inverted;}
    this.x=Math.max(0,Math.min(128-tw,this.x));
    this.y=Math.max(0,Math.min(64-th,this.y));
  }
  draw(fb) {
    const ix=Math.floor(this.x),iy=Math.floor(this.y);
    const tw=Font.textWidth('TinyOLED');
    if(this.inverted) {
      fb.rect(ix-2,iy-2,tw+4,11,true,true);
      fb.text('TinyOLED',ix,iy,false);
    } else {
      fb.text('TinyOLED',ix,iy);
      fb.rect(ix-2,iy-2,tw+4,11);
    }
  }
}
