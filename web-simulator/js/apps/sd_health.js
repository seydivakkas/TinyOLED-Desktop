import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';
export class SDHealthApp extends BrowserApp {
  static NAME='sd'; static LABEL='SD'; static ICON='sd';
  constructor(onExit){super(onExit,{title:'Depolama',mode:'WEB/BRG'});this.browser={};this.pi={};this._web();}
  async _web(){if(navigator.storage?.estimate){const e=await navigator.storage.estimate();this.browser={used:e.usage,total:e.quota};}}
  async onSel(){await this.task(async()=>{configureBridge();this.pi=await bridgeJSON('/api/storage');this.status='Pi storage';},'depolama');}
  draw(fb){this.drawHeader(fb,'WEB');const mb=x=>x==null?'--':`${Math.round(x/1048576)}M`;this.drawRows(fb,[['Web used',mb(this.browser.used)],['Web quota',mb(this.browser.total)],['Pi used',this.pi.used_percent!=null?`${this.pi.used_percent}%`:'--'],['Pi free',this.pi.free||'--']]);this.footer(fb,'SEL Pi bridge');}
}
