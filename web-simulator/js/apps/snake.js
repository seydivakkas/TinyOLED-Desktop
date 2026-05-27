/** TinyOLED Desktop — Snake Game */
const BLOCK=4, AREA_Y=10, AREA_H=54;

export class SnakeApp {
  static NAME='snake'; static LABEL='Yilan'; static ICON='snake';
  constructor(onExit) { this.onExit=onExit; this.reset(); }
  reset() {
    this.snake=[[64,32],[60,32],[56,32]];
    this.dir=[BLOCK,0]; this.food=this._randFood();
    this.score=0; this.gameOver=false; this._last=0;
  }
  _randFood() { return [2+Math.floor(Math.random()*29)*BLOCK, (3+Math.floor(Math.random()*12))*BLOCK]; }
  onUp()   { if(!this.gameOver){const[dx,dy]=this.dir;this.dir=[-dy,dx];} }
  onDown() { if(!this.gameOver){const[dx,dy]=this.dir;this.dir=[dy,-dx];} }
  onSel()  { if(this.gameOver) this.reset(); }
  onLong() { this.onExit(); }

  update() {
    if(this.gameOver) return;
    const now=performance.now()/1000;
    if(now-this._last<0.15) return;
    this._last=now;
    const hx=(this.snake[0][0]+this.dir[0]+128)%128;
    const hy=((this.snake[0][1]-AREA_Y+this.dir[1]+AREA_H)%AREA_H)+AREA_Y;
    const head=[hx,hy];
    if(this.snake.some(s=>s[0]===hx&&s[1]===hy)) { this.gameOver=true; return; }
    this.snake.unshift(head);
    if(Math.abs(hx-this.food[0])<BLOCK && Math.abs(hy-this.food[1])<BLOCK) {
      this.score++; this.food=this._randFood();
    } else this.snake.pop();
  }

  draw(fb) {
    fb.text(`Skor:${this.score}`,2,AREA_Y);
    fb.hline(0,AREA_Y+8,128);
    if(this.gameOver) {
      fb.textCentered('OYUN BITTI!',28);
      fb.textCentered(`Skor: ${this.score}`,38);
      fb.textCentered('[SEL] Tekrar',50);
      return;
    }
    fb.rect(this.food[0],this.food[1],BLOCK-1,BLOCK-1,true,true);
    this.snake.forEach(([x,y],i)=>fb.rect(x,y,BLOCK-1,BLOCK-1,true,i!==0));
  }
}
