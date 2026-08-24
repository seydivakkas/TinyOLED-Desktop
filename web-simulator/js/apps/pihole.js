import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';
export class PiHoleApp extends BrowserApp {
  static NAME='pihole'; static LABEL='PiHole'; static ICON='pihole';
  constructor(onExit){super(onExit,{title:'Pi-hole',mode:'BRG'});this.data={};}
  async refresh(){configureBridge();this.data=await bridgeJSON('/api/pihole');}
  async onSel(){await this.task(async()=>{if(this.data.enabled===undefined){await this.refresh();return;}await bridgeJSON('/api/pihole/toggle',{method:'POST',body:{enabled:!this.data.enabled}});await this.refresh();},'Pi-hole');}
  draw(fb){this.drawHeader(fb,'BRG');this.drawRows(fb,[['Durum',this.data.enabled?'ON':this.data.enabled===false?'OFF':'--'],['Engel',this.data.blocked??'--'],['DNS',this.data.queries??'--'],['Oran',this.data.percent!=null?`${this.data.percent}%`:'--']]);this.footer(fb,'SEL oku/toggle');}
}
