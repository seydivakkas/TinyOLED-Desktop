import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';
export class WiFiScannerApp extends BrowserApp {
  static NAME='wifiscan'; static LABEL='WiScan'; static ICON='radar';
  constructor(onExit){super(onExit,{title:'WiFi Scan',mode:'BRG'});this.networks=[];this.cursor=0;}
  onUp(){if(this.networks.length)this.cursor=(this.cursor-1+this.networks.length)%this.networks.length;}
  onDown(){if(this.networks.length)this.cursor=(this.cursor+1)%this.networks.length;}
  async onSel(){await this.task(async()=>{configureBridge();const d=await bridgeJSON('/api/wifi/scan');this.networks=(d.networks||[]).sort((a,b)=>(b.signal||-999)-(a.signal||-999));this.cursor=0;this.status=`${this.networks.length} ag`;},'taranıyor');}
  draw(fb){this.drawHeader(fb,'BRG');const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,this.networks.length-4)));this.drawRows(fb,this.networks.length?this.networks.slice(start,start+4).map(n=>[n.ssid||'SSID',`${n.channel??'?'} ${n.signal??'?'}dB`]):[['SEL','ag tara'],['API','local bridge']],this.cursor-start);this.footer(fb,'SEL tara');}
}
