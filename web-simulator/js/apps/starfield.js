/** TinyOLED Desktop — Starfield Screensaver */
export class StarfieldApp {
  static NAME='starfield'; static LABEL='Yldiz'; static ICON='star';
  constructor(onExit) {
    this.onExit=onExit; this._last=0;
    this.stars=Array.from({length:40},()=>[Math.random()*2-1,Math.random()*2-1,Math.random()*0.9+0.1]);
  }
  onUp(){} onDown(){} onSel(){} onLong(){this.onExit();}
  update() {
    const now=performance.now()/1000;
    if(now-this._last<0.05) return;
    this._last=now;
    for(let i=0;i<this.stars.length;i++) {
      let[x,y,z]=this.stars[i]; z-=0.02;
      if(z<=0) this.stars[i]=[Math.random()*2-1,Math.random()*2-1,1.0];
      else this.stars[i]=[x,y,z];
    }
  }
  draw(fb) {
    for(const[x,y,z] of this.stars) {
      if(z<=0) continue;
      const sx=Math.floor(64+x*80/z), sy=Math.floor(32+y*40/z);
      if(sx>=0&&sx<128&&sy>=0&&sy<64) {
        fb.pixel(sx,sy);
        if(z<0.3){fb.pixel(sx+1,sy);fb.pixel(sx,sy+1);}
      }
    }
  }
}
