import { BrowserApp } from '../browser_app.js';
import { ioCommand } from '../browser_bridge.js';
export class PlantMonitorApp extends BrowserApp {
  static NAME='plant'; static LABEL='Bitki'; static ICON='plant';
  constructor(onExit){super(onExit,{title:'Bitki',mode:'SER/BRG'});this.data={};}
  async refresh(){this.data=await ioCommand({cmd:'plant.read'});}
  async onSel(){await this.task(async()=>{if(this.data.moisture==null){await this.refresh();return;}await ioCommand({cmd:'plant.pump',on:!this.data.pump});await this.refresh();},'bitki');}
  draw(fb){this.drawHeader(fb,'SER');this.drawRows(fb,[['Nem',this.data.moisture!=null?`${this.data.moisture}%`:'--'],['Esik',this.data.threshold!=null?`${this.data.threshold}%`:'--'],['Pompa',this.data.pump?'ON':'OFF'],['Durum',this.data.state||'--']]);this.footer(fb,'SEL oku/toggle');}
}
