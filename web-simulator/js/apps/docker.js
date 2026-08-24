import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';
export class DockerApp extends BrowserApp {
  static NAME='docker'; static LABEL='Docker'; static ICON='docker';
  constructor(onExit){super(onExit,{title:'Docker',mode:'BRG'});this.containers=[];this.cursor=0;}
  onUp(){if(this.containers.length)this.cursor=(this.cursor-1+this.containers.length)%this.containers.length;}
  onDown(){if(this.containers.length)this.cursor=(this.cursor+1)%this.containers.length;}
  async refresh(){configureBridge();const d=await bridgeJSON('/api/docker');this.containers=d.containers||[];this.cursor=Math.min(this.cursor,Math.max(0,this.containers.length-1));}
  async onSel(){await this.task(async()=>{if(!this.containers.length){await this.refresh();return;}const c=this.containers[this.cursor];await bridgeJSON('/api/docker/action',{method:'POST',body:{id:c.id,action:c.running?'stop':'start'}});await this.refresh();},'docker');}
  draw(fb){this.drawHeader(fb,'BRG');const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,this.containers.length-4)));this.drawRows(fb,this.containers.length?this.containers.slice(start,start+4).map(c=>[c.running?'RUN':'STOP',c.name]):[['SEL','listele']],this.cursor-start);this.footer(fb,'SEL list/toggle');}
}
