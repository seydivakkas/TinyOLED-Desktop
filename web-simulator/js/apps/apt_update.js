import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';
export class APTUpdateApp extends BrowserApp {
  static NAME='apt'; static LABEL='APT'; static ICON='apt';
  constructor(onExit){super(onExit,{title:'APT',mode:'BRG'});this.data={};}
  async onSel(){await this.task(async()=>{configureBridge();this.data=await bridgeJSON('/api/apt/updates');this.status='liste';},'apt');}
  draw(fb){this.drawHeader(fb,'BRG');this.drawRows(fb,[['Bekleyen',this.data.pending??'--'],['Guvenlik',this.data.security??'--'],['Son',this.data.last_check||'--'],['Aksiyon','read-only']]);this.footer(fb,'SEL kontrol');}
}
