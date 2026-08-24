import { BrowserApp } from '../browser_app.js';
import { ioCommand } from '../browser_bridge.js';
export class UPSBatteryApp extends BrowserApp {
  static NAME='ups'; static LABEL='UPS'; static ICON='ups';
  constructor(onExit){super(onExit,{title:'UPS Pil',mode:'WEB/SER'});this.browserBattery=null;this.ups={};this._battery();}
  async _battery(){if(navigator.getBattery)this.browserBattery=await navigator.getBattery().catch(()=>null);}
  async onSel(){await this.task(async()=>{this.ups=await ioCommand({cmd:'ups.read'});this.status='UPS';},'UPS');}
  draw(fb){this.drawHeader(fb,'WEB');this.drawRows(fb,[['Browser',this.browserBattery?`${Math.round(this.browserBattery.level*100)}%`:'n/a'],['UPS',this.ups.percent!=null?`${this.ups.percent}%`:'--'],['Volt',this.ups.voltage!=null?`${this.ups.voltage}V`:'--'],['Sarj',this.ups.charging?'ON':'--']]);this.footer(fb,'SEL UPS bridge');}
}
