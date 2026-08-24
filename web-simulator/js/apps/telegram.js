import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';
export class TelegramApp extends BrowserApp {
  static NAME='telegram'; static LABEL='Tele'; static ICON='telegram';
  constructor(onExit){super(onExit,{title:'Telegram',mode:'BRG'});this.messages=[];this.cursor=0;}
  onUp(){if(this.messages.length)this.cursor=(this.cursor-1+this.messages.length)%this.messages.length;}
  onDown(){if(this.messages.length)this.cursor=(this.cursor+1)%this.messages.length;}
  async onSel(){await this.task(async()=>{configureBridge();const d=await bridgeJSON('/api/telegram/messages');this.messages=d.messages||[];this.cursor=0;this.status=`${this.messages.length} msg`;},'Telegram');}
  draw(fb){this.drawHeader(fb,'BRG');const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,this.messages.length-4)));this.drawRows(fb,this.messages.length?this.messages.slice(start,start+4).map(m=>[m.from||'user',m.text||'']):[['SEL','bridge Bot API'],['Token','server-side']],this.cursor-start);this.footer(fb,'SEL yenile');}
}
