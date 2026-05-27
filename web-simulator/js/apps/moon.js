/** TinyOLED Desktop — Moon Phase Display */
const NAMES=['Yeni Ay','Hilal','Ilk Dordun','Siskin','Dolunay','Siskin','Son Dordun','Hilal'];

export class MoonApp {
  static NAME='moon'; static LABEL='Ay'; static ICON='moon';
  constructor(onExit){this.onExit=onExit;this.phase=0;}
  onUp(){} onDown(){} onSel(){} onLong(){this.onExit();}
  update() {
    const ref=947182800, synodic=29.53058867;
    this.phase=((Date.now()/1000-ref)/86400%synodic)/synodic;
  }
  draw(fb) {
    fb.text('Ay Evresi',30,2);
    const cx=40,cy=36,r=16;
    fb.circle(cx,cy,r,true,true);
    const illum=this.phase<=0.5?this.phase*2:(1-this.phase)*2;
    for(let dy=-r;dy<=r;dy++) {
      const hw=Math.floor(Math.sqrt(Math.max(0,r*r-dy*dy)));
      const sw=Math.floor(hw*(1-illum));
      if(this.phase<=0.5) { for(let sx=-hw;sx<-hw+sw;sx++) fb.pixel(cx+sx,cy+dy,false); }
      else { for(let sx=hw-sw;sx<=hw;sx++) fb.pixel(cx+sx,cy+dy,false); }
    }
    fb.circle(cx,cy,r);
    const idx=Math.floor(this.phase*8)%8;
    fb.text(NAMES[idx],65,28);
    fb.text(`%${Math.floor(illum*100)} aydinlik`,65,40);
    fb.text(`Gun:${(this.phase*29.53).toFixed(1)}/29.5`,65,52);
  }
}
