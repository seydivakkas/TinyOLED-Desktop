import { BrowserApp } from '../browser_app.js';
import { ioCommand } from '../browser_bridge.js';
export class GPIOViewerApp extends BrowserApp {
  static NAME='gpio'; static LABEL='GPIO'; static ICON='pin';
  constructor(onExit){super(onExit,{title:'GPIO',mode:'SER/BRG'});this.pins=[];this.cursor=0;}
  onUp(){if(this.pins.length)this.cursor=(this.cursor-1+this.pins.length)%this.pins.length;}
  onDown(){if(this.pins.length)this.cursor=(this.cursor+1)%this.pins.length;}
  async refresh(){const d=await ioCommand({cmd:'gpio.list'});this.pins=d.pins||[];}
  async onSel(){await this.task(async()=>{if(!this.pins.length){await this.refresh();return;}const p=this.pins[this.cursor];if(p.direction==='out'){await ioCommand({cmd:'gpio.write',pin:p.pin,value:p.value?0:1});await this.refresh();}else this.status='input pin';},'GPIO');}
  draw(fb){this.drawHeader(fb,'SER');const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,this.pins.length-4)));this.drawRows(fb,this.pins.length?this.pins.slice(start,start+4).map(p=>[`G${p.pin}`,`${p.direction||'?'} ${p.value?1:0}`]):[['SEL','serial/bridge'],['Proto','JSON line']],this.cursor-start);this.footer(fb,'SEL list/toggle');}
}
