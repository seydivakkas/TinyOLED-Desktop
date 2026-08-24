import { BrowserApp } from '../browser_app.js';
import { ioCommand } from '../browser_bridge.js';
export class TemperatureHumidityApp extends BrowserApp {
  static NAME='temp'; static LABEL='Temp'; static ICON='temp';
  constructor(onExit){super(onExit,{title:'Sicak/Nem',mode:'SER/BRG'});this.data={};}
  async onSel(){await this.task(async()=>{this.data=await ioCommand({cmd:'dht.read'});this.status='sensor';},'DHT');}
  draw(fb){this.drawHeader(fb,'SER');this.drawRows(fb,[['Sicak',this.data.temperature!=null?`${Number(this.data.temperature).toFixed(1)}C`:'--'],['Nem',this.data.humidity!=null?`${Number(this.data.humidity).toFixed(1)}%`:'--'],['Sensor',this.data.sensor||'DHT22'],['Durum',this.status]]);this.footer(fb,'SEL oku');}
}
