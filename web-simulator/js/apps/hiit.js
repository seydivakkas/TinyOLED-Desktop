import { BrowserApp } from '../browser_app.js';
const PRESETS=[['Tabata',20,10,8],['HIIT',30,15,8],['Sprint',40,20,6]];

export class HIITTimerApp extends BrowserApp {
  static NAME='hiit'; static LABEL='HIIT'; static ICON='workout';
  constructor(onExit){super(onExit,{title:'HIIT',mode:'WEB'});this.preset=0;this.running=false;this.phase='READY';this.round=1;this.ends=0;}
  onUp(){if(!this.running)this.preset=(this.preset-1+PRESETS.length)%PRESETS.length;}
  onDown(){if(!this.running)this.preset=(this.preset+1)%PRESETS.length;}
  onSel(){if(this.running){this.running=false;this.status='pause';return;}this.running=true;if(this.phase==='READY'||this.phase==='DONE')this._startWork();else this.ends=performance.now()+this.remaining*1000;}
  _startWork(){const [,work,,]=PRESETS[this.preset];this.phase='WORK';this.ends=performance.now()+work*1000;}
  _startRest(){const [,,rest,]=PRESETS[this.preset];this.phase='REST';this.ends=performance.now()+rest*1000;}
  update(){super.update();if(!this.running)return;const left=Math.ceil((this.ends-performance.now())/1000);this.remaining=Math.max(0,left);if(left<=0){const [,,,rounds]=PRESETS[this.preset];if(this.phase==='WORK')this._startRest();else if(this.round>=rounds){this.running=false;this.phase='DONE';}else{this.round++;this._startWork();}}}
  draw(fb){this.drawHeader(fb,'WEB');const [name,w,r,rounds]=PRESETS[this.preset];this.drawRows(fb,[['Plan',name],['Faz',this.phase],['Kalan',`${this.remaining??w}s`],['Tur',`${this.round}/${rounds}`]]);this.footer(fb,'SEL baslat/pause');}
}
