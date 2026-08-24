import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';

export class WiFiApp extends BrowserApp {
  static NAME='wifi'; static LABEL='WiFi'; static ICON='radar';
  constructor(onExit){super(onExit,{title:'WiFi',mode:'WEB/BRG'});this.networks=[];this.cursor=0;this.connection=navigator.connection||null;}
  onUp(){if(this.networks.length)this.cursor=(this.cursor-1+this.networks.length)%this.networks.length;}
  onDown(){if(this.networks.length)this.cursor=(this.cursor+1)%this.networks.length;}
  async onSel(){
    await this.task(async()=>{
      configureBridge();
      if(!this.networks.length){
        const d=await bridgeJSON('/api/wifi/scan');
        this.networks=(d.networks||[]).slice(0,12);this.cursor=0;this.status='tarandi';return;
      }
      const n=this.networks[this.cursor];
      const password=prompt(`${n.ssid||'Ag'} parolasi (bridge'e gonderilir, kaydedilmez)`,'');
      if(password===null)return;
      await bridgeJSON('/api/wifi/connect',{method:'POST',body:{ssid:n.ssid,password}});
      this.status='baglanti istendi';
    },'WiFi');
  }
  draw(fb){
    this.drawHeader(fb,'BRG');
    if(this.networks.length){
      const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,this.networks.length-4)));
      this.drawRows(fb,this.networks.slice(start,start+4).map(n=>[n.ssid||'SSID',`${n.signal??'--'}dB`]),this.cursor-start);
    }else{
      const c=this.connection;this.drawRows(fb,[['Tip',c?.effectiveType||'n/a'],['Down',c?.downlink?`${c.downlink}Mb`:'n/a'],['RTT',c?.rtt?`${c.rtt}ms`:'n/a'],['SEL','bridge scan']]);
    }
    this.footer(fb,'SEL tara/baglan');
  }
}
