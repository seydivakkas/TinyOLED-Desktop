import { BrowserApp, loadJSON, saveJSON } from '../browser_app.js';
const KEY='tinyoled.pixelart.v1', W=32, H=11;

export class PixelArtApp extends BrowserApp {
  static NAME='pixel'; static LABEL='Pixel'; static ICON='paint';
  constructor(onExit){super(onExit,{title:'Pixel Art',mode:'WEB'});this.bits=loadJSON(KEY,Array(W*H).fill(0));this.cursor=0;}
  onUp(){this.cursor=(this.cursor-1+W*H)%(W*H);}
  onDown(){this.cursor=(this.cursor+1)%(W*H);}
  onSel(){this.bits[this.cursor]=this.bits[this.cursor]?0:1;saveJSON(KEY,this.bits);this.status='kayit';}
  draw(fb){
    this.drawHeader(fb,'WEB');
    for(let y=0;y<H;y++)for(let x=0;x<W;x++){const i=y*W+x;if(this.bits[i])fb.rect(x*4,21+y*3,4,3,true,true);}
    const cx=(this.cursor%W)*4, cy=21+Math.floor(this.cursor/W)*3; fb.rect(cx,cy,4,3,true,false);
    this.footer(fb,'UP/DN pixel SEL boya');
  }
}
