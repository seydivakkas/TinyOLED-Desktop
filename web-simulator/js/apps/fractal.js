/** TinyOLED Desktop — Mandelbrot Fractal Explorer */
export class FractalApp {
  static NAME='fractal'; static LABEL='Fraktl'; static ICON='fractal';
  constructor(onExit) { this.onExit=onExit; this.cx=-0.5; this.cy=0; this.zoom=1.5; this.maxIter=20; }
  onUp()   { this.zoom*=0.7; this.maxIter=Math.min(50,this.maxIter+2); }
  onDown() { this.zoom*=1.4; this.maxIter=Math.max(10,this.maxIter-2); }
  onSel()  { this.cx=-0.5; this.cy=0; this.zoom=1.5; this.maxIter=20; }
  onLong() { this.onExit(); }
  update() {}
  draw(fb) {
    for(let py=0;py<64;py++) {
      for(let px=0;px<128;px++) {
        const x0=this.cx+(px-64)*this.zoom/64;
        const y0=this.cy+(py-32)*this.zoom/32;
        let x=0,y=0,i=0;
        while(x*x+y*y<=4 && i<this.maxIter) { const t=x*x-y*y+x0; y=2*x*y+y0; x=t; i++; }
        if(i<this.maxIter) fb.pixel(px,py);
      }
    }
  }
}
