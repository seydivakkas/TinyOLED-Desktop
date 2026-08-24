import { BrowserApp } from '../browser_app.js';
import { ioCommand } from '../browser_bridge.js';
export class I2CScannerApp extends BrowserApp {
  static NAME='i2c'; static LABEL='I2C'; static ICON='i2c';
  constructor(onExit){super(onExit,{title:'I2C Scan',mode:'SER/BRG'});this.devices=[];this.cursor=0;}
  onUp(){if(this.devices.length)this.cursor=(this.cursor-1+this.devices.length)%this.devices.length;}
  onDown(){if(this.devices.length)this.cursor=(this.cursor+1)%this.devices.length;}
  async onSel(){await this.task(async()=>{const d=await ioCommand({cmd:'i2c.scan',bus:1});this.devices=d.devices||[];this.cursor=0;this.status=`${this.devices.length} cihaz`;},'I2C');}
  draw(fb){this.drawHeader(fb,'SER');const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,this.devices.length-4)));this.drawRows(fb,this.devices.length?this.devices.slice(start,start+4).map(d=>[d.address||'addr',d.name||'device']):[['SEL','bus tara'],['Bus','1']],this.cursor-start);this.footer(fb,'SEL tara');}
}
