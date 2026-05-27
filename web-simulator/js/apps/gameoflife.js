/** TinyOLED Desktop — Conway's Game of Life */
const W=128, H=64;

export class GameOfLifeApp {
  static NAME='life'; static LABEL='Life'; static ICON='cell';
  constructor(onExit) { this.onExit=onExit; this._last=0; this.gen=0; this.randomize(); }
  randomize() {
    this.grid=Array.from({length:H},()=>Array.from({length:W},()=>Math.random()<0.3));
    this.gen=0;
  }
  onUp(){} onDown(){} onSel(){this.randomize();} onLong(){this.onExit();}
  _neighbors(x,y) {
    let c=0;
    for(let dy=-1;dy<=1;dy++) for(let dx=-1;dx<=1;dx++) {
      if(!dx&&!dy) continue;
      if(this.grid[(y+dy+H)%H][(x+dx+W)%W]) c++;
    }
    return c;
  }
  update() {
    const now=performance.now()/1000;
    if(now-this._last<0.15) return;
    this._last=now; this.gen++;
    const ng=Array.from({length:H},()=>new Array(W).fill(false));
    for(let y=0;y<H;y++) for(let x=0;x<W;x++) {
      const n=this._neighbors(x,y);
      if(this.grid[y][x]) ng[y][x]=(n===2||n===3);
      else ng[y][x]=(n===3);
    }
    this.grid=ng;
  }
  draw(fb) {
    for(let y=0;y<H;y++) for(let x=0;x<W;x++) if(this.grid[y][x]) fb.pixel(x,y);
  }
}
