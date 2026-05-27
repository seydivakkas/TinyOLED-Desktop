/** TinyOLED Desktop — Flappy Bird */
export class FlappyApp {
  static NAME='flappy'; static LABEL='Flappy'; static ICON='bird';
  constructor(onExit) { this.onExit=onExit; this.reset(); }
  reset() {
    this.birdY=32; this.vel=0; this.gravity=0.8;
    this.pipes=[]; this.score=0; this.gameOver=false; this.frame=0; this._last=0;
    this._addPipe(128);
  }
  _addPipe(x) {
    const gapY=18+Math.floor(Math.random()*28), gapH=20;
    this.pipes.push({x, gapY, gapH, scored:false});
  }
  _flap() { if(!this.gameOver) this.vel=-4.5; }
  onUp()   { this._flap(); }
  onDown() {}
  onSel()  { if(this.gameOver) this.reset(); else this._flap(); }
  onLong() { this.onExit(); }

  update() {
    if(this.gameOver) return;
    const now=performance.now()/1000;
    if(now-this._last<0.05) return;
    this._last=now;
    this.vel+=this.gravity; this.birdY+=this.vel;
    if(this.birdY<10||this.birdY>62) { this.gameOver=true; return; }
    for(const p of this.pipes) {
      p.x-=2;
      if(!p.scored && p.x<20) { p.scored=true; this.score++; }
      if(p.x+6>17 && p.x<23) {
        const by=Math.floor(this.birdY);
        if(by-3<p.gapY || by+3>p.gapY+p.gapH) { this.gameOver=true; return; }
      }
    }
    this.pipes=this.pipes.filter(p=>p.x>-10);
    if(!this.pipes.length || this.pipes[this.pipes.length-1].x<80) this._addPipe(130);
  }

  draw(fb) {
    fb.text(`Skor:${this.score}`,50,2);
    if(this.gameOver) {
      fb.textCentered('GAME OVER',24);
      fb.textCentered(`Skor: ${this.score}`,34);
      fb.textCentered('[SEL] Tekrar',46);
      return;
    }
    const by=Math.floor(this.birdY);
    fb.circle(20,by,3,true,true);
    fb.pixel(24,by-1); fb.pixel(24,by);
    for(const p of this.pipes) {
      const px=Math.floor(p.x);
      fb.rect(px,10,6,p.gapY-10,true,true);
      fb.rect(px,p.gapY+p.gapH,6,64-p.gapY-p.gapH,true,true);
    }
    fb.hline(0,9,128);
  }
}
