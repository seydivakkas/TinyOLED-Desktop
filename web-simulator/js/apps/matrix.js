/** TinyOLED Desktop — Matrix Digital Rain */
const COLS=21, ROWS=8;

export class MatrixRainApp {
  static NAME='matrix'; static LABEL='Matrx'; static ICON='matrix';
  constructor(onExit) {
    this.onExit=onExit; this._last=0;
    this.drops=Array.from({length:COLS},()=>Math.floor(Math.random()*(ROWS+4))-ROWS);
    this.chars=Array.from({length:COLS},()=>Array.from({length:ROWS},()=>33+Math.floor(Math.random()*93)));
  }
  onUp(){} onDown(){} onSel(){} onLong(){this.onExit();}
  update() {
    const now=performance.now()/1000;
    if(now-this._last<0.1) return;
    this._last=now;
    for(let c=0;c<COLS;c++) {
      this.drops[c]++;
      if(this.drops[c]>ROWS+4) this.drops[c]=Math.floor(Math.random()*5)-4;
      this.chars[c][((this.drops[c]%ROWS)+ROWS)%ROWS]=33+Math.floor(Math.random()*93);
    }
  }
  draw(fb) {
    for(let c=0;c<COLS;c++) {
      const x=c*6+1, dropY=this.drops[c];
      for(let r=0;r<ROWS;r++) {
        if(r<=dropY && r>dropY-5) {
          const ch=String.fromCharCode(this.chars[c][((r%ROWS)+ROWS)%ROWS]);
          const y=r*8;
          if(r===dropY) {
            fb.rect(x-1,y-1,7,9,true,true);
            fb.text(ch,x,y,false);
          } else {
            fb.text(ch,x,y);
          }
        }
      }
    }
  }
}
