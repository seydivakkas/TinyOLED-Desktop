/** TinyOLED Desktop — Breathing Exercise */
const PHASES=[['NEFES AL',4],['TUT',7],['NEFES VER',8]];

export class BreathingApp {
  static NAME='breath'; static LABEL='Nefes'; static ICON='breath';
  constructor(onExit) {
    this.onExit=onExit; this.running=false; this.phase=0; this.start=0; this.cycles=0;
  }
  onUp(){} onDown(){}
  onSel() {
    if(!this.running){this.running=true;this.phase=0;this.start=performance.now()/1000;this.cycles=0;}
    else this.running=false;
  }
  onLong(){this.onExit();}
  update() {
    if(!this.running) return;
    const elapsed=performance.now()/1000-this.start;
    if(elapsed>=PHASES[this.phase][1]) {
      this.phase++;
      if(this.phase>=PHASES.length){this.phase=0;this.cycles++;}
      this.start=performance.now()/1000;
    }
  }
  draw(fb) {
    if(!this.running) {
      fb.textCentered('Nefes Egzersizi',14);
      fb.textCentered('4-7-8 Teknigi',26);
      fb.textCentered('[SEL] Basla',42);
      return;
    }
    const[name,dur]=PHASES[this.phase];
    const elapsed=performance.now()/1000-this.start;
    const prog=Math.min(1,elapsed/dur), rem=Math.max(0,dur-elapsed);
    fb.textCentered(name,10);
    const cx=64,cy=38,mn=4,mx=22;
    let r;
    if(this.phase===0) r=Math.round(mn+(mx-mn)*prog);
    else if(this.phase===1) r=mx+Math.round(Math.sin(elapsed*6)*1.5);
    else r=Math.round(mx-(mx-mn)*prog);
    fb.circle(cx,cy,r,true,true);
    fb.circle(cx,cy,mx+2);
    fb.text(`${Math.floor(rem)}s`,110,34);
    fb.text(`Dongu:${this.cycles}`,2,56);
  }
}
