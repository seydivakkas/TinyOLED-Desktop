import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';
export class SystemdApp extends BrowserApp {
  static NAME='systemd'; static LABEL='Svc'; static ICON='service';
  constructor(onExit){super(onExit,{title:'systemd',mode:'BRG'});this.services=[];this.cursor=0;}
  onUp(){if(this.services.length)this.cursor=(this.cursor-1+this.services.length)%this.services.length;}
  onDown(){if(this.services.length)this.cursor=(this.cursor+1)%this.services.length;}
  async refresh(){configureBridge();const d=await bridgeJSON('/api/systemd');this.services=d.services||[];}
  async onSel(){await this.task(async()=>{if(!this.services.length){await this.refresh();return;}const s=this.services[this.cursor];if(confirm(`${s.name} servisini yeniden baslat?`)){await bridgeJSON('/api/systemd/restart',{method:'POST',body:{service:s.name}});await this.refresh();}},'systemd');}
  draw(fb){this.drawHeader(fb,'BRG');const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,this.services.length-4)));this.drawRows(fb,this.services.length?this.services.slice(start,start+4).map(s=>[s.active?'ON':'OFF',s.name]):[['SEL','servis listele']],this.cursor-start);this.footer(fb,'SEL list/restart');}
}
