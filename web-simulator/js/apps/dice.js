/** TinyOLED Desktop — Dice Simulator */
import { Font } from '../font.js';
const DICE_TYPES=[4,6,8,10,12,20];

export class DiceApp {
  static NAME='dice'; static LABEL='Zar'; static ICON='dice';
  constructor(onExit) {
    this.onExit=onExit; this._typeIdx=1; this.result=0;
    this._rolling=false; this._rollFrames=0; this._last=0;
  }
  onUp()   { this._typeIdx=(this._typeIdx-1+DICE_TYPES.length)%DICE_TYPES.length; }
  onDown() { this._typeIdx=(this._typeIdx+1)%DICE_TYPES.length; }
  onSel()  { if(!this._rolling){this._rolling=true;this._rollFrames=0;} }
  onLong() { this.onExit(); }

  update() {
    if(!this._rolling) return;
    const now=performance.now()/1000;
    if(now-this._last<0.05) return;
    this._last=now; this._rollFrames++;
    this.result=1+Math.floor(Math.random()*DICE_TYPES[this._typeIdx]);
    if(this._rollFrames>=20) this._rolling=false;
  }

  draw(fb) {
    const sides=DICE_TYPES[this._typeIdx];
    fb.text(`Zar: D${sides}`,2,10); fb.hline(0,18,128);
    for(let i=0;i<DICE_TYPES.length;i++) {
      const x=4+i*21, sel=(i===this._typeIdx);
      if(sel) fb.rect(x-1,20,20,10,true,true);
      fb.text(`D${DICE_TYPES[i]}`,x,21,!sel);
    }
    if(this.result>0) {
      const rStr=String(this.result), scale=4;
      let sx=Math.floor((128-rStr.length*6*scale)/2);
      for(const ch of rStr) {
        const cols=Font.glyph(ch);
        for(let ci=0;ci<cols.length;ci++)
          for(let ri=0;ri<7;ri++)
            if(cols[ci]&(1<<ri)) fb.rect(sx+ci*scale,34+ri*scale,scale,scale,true,true);
        sx+=6*scale;
      }
    }
    fb.text(this._rolling?'Yuvarlaniyor...':'[SEL] At',2,56);
  }
}
