import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';
const COMMANDS=[['uptime','Uptime'],['disk','Disk'],['memory','Memory'],['network','Network']];
export class CommandRunnerApp extends BrowserApp {
  static NAME='script'; static LABEL='Komut'; static ICON='script';
  constructor(onExit){super(onExit,{title:'Komut',mode:'BRG'});this.cursor=0;this.output='--';}
  onUp(){this.cursor=(this.cursor-1+COMMANDS.length)%COMMANDS.length;}
  onDown(){this.cursor=(this.cursor+1)%COMMANDS.length;}
  async onSel(){await this.task(async()=>{configureBridge();const [id]=COMMANDS[this.cursor];const d=await bridgeJSON('/api/commands/run',{method:'POST',body:{id}});this.output=String(d.output||d.result||'ok').replace(/\s+/g,' ');this.status='tamam';},'calisiyor');}
  draw(fb){this.drawHeader(fb,'BRG');this.drawRows(fb,[['Komut',COMMANDS[this.cursor][1]],['Cikis',this.output.slice(0,11)],['Guvenlik','allow-list'],['Shell','bridge']]);this.footer(fb,'UP/DN sec SEL run');}
}
