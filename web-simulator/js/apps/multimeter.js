import { BrowserApp } from '../browser_app.js';
import { ioCommand } from '../browser_bridge.js';
export class MultimeterApp extends BrowserApp {
  static NAME='meter'; static LABEL='Metre'; static ICON='volt';
  constructor(onExit){super(onExit,{title:'Multimetre',mode:'SER/BRG'});this.data={};}
  async onSel(){await this.task(async()=>{this.data=await ioCommand({cmd:'ina219.read'});this.status='olculdu';},'INA219');}
  draw(fb){this.drawHeader(fb,'SER');this.drawRows(fb,[['Volt',this.data.voltage!=null?`${Number(this.data.voltage).toFixed(2)}V`:'--'],['Akim',this.data.current!=null?`${Number(this.data.current).toFixed(0)}mA`:'--'],['Guc',this.data.power!=null?`${Number(this.data.power).toFixed(2)}W`:'--'],['Sensor','INA219']]);this.footer(fb,'SEL oku');}
}
