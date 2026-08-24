import { BrowserApp, clamp } from '../browser_app.js';

export class GraphApp extends BrowserApp {
  static NAME='graph'; static LABEL='Grafik'; static ICON='graph';
  constructor(onExit){
    super(onExit,{title:'Browser Graph',mode:'WEB'});
    this.metrics=['Lag','Heap','Net'];
    this.cursor=0; this.samples=[]; this.last=performance.now();
  }
  onUp(){this.cursor=(this.cursor-1+this.metrics.length)%this.metrics.length; this.samples=[];}
  onDown(){this.cursor=(this.cursor+1)%this.metrics.length; this.samples=[];}
  onSel(){this.samples=[]; this.status='sifirlandi';}
  update(){
    super.update();
    if(this._tick%4!==0) return;
    const now=performance.now();
    let value=0;
    if(this.metrics[this.cursor]==='Lag'){
      value=clamp(Math.abs((now-this.last)-200),0,100);
      this.last=now;
    } else if(this.metrics[this.cursor]==='Heap'){
      const mem=performance.memory;
      value=mem?.jsHeapSizeLimit ? (mem.usedJSHeapSize/mem.jsHeapSizeLimit)*100 : 0;
    } else {
      value=clamp((navigator.connection?.downlink || 0)*5,0,100);
    }
    this.samples.push(value); if(this.samples.length>100) this.samples.shift();
  }
  draw(fb){
    this.drawHeader(fb,'WEB');
    fb.text(`${this.metrics[this.cursor]} ${this.samples.at(-1)?.toFixed(1) ?? '--'}`,2,22);
    fb.rect(2,31,124,22);
    if(this.samples.length>1){
      for(let i=1;i<this.samples.length;i++){
        const x0=3+Math.floor((i-1)*121/99), x1=3+Math.floor(i*121/99);
        const y0=51-Math.floor(clamp(this.samples[i-1],0,100)*18/100);
        const y1=51-Math.floor(clamp(this.samples[i],0,100)*18/100);
        fb.line(x0,y0,x1,y1);
      }
    }
    this.footer(fb,'UP/DN metrik SEL reset');
  }
}
