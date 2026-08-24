import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';
export class SSHAlertApp extends BrowserApp {
  static NAME='ssh'; static LABEL='SSH'; static ICON='shield';
  constructor(onExit){super(onExit,{title:'SSH Uyari',mode:'BRG'});this.alerts=[];this.cursor=0;}
  onUp(){if(this.alerts.length)this.cursor=(this.cursor-1+this.alerts.length)%this.alerts.length;}
  onDown(){if(this.alerts.length)this.cursor=(this.cursor+1)%this.alerts.length;}
  async onSel(){await this.task(async()=>{configureBridge();const d=await bridgeJSON('/api/ssh/alerts');this.alerts=d.alerts||[];this.cursor=0;this.status=`${this.alerts.length} olay`;},'log');}
  draw(fb){this.drawHeader(fb,'BRG');const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,this.alerts.length-4)));this.drawRows(fb,this.alerts.length?this.alerts.slice(start,start+4).map(a=>[a.count||1,a.ip||a.user||'event']):[['SEL','auth log oku'],['Kaynak','local bridge']],this.cursor-start);this.footer(fb,'SEL yenile');}
}
