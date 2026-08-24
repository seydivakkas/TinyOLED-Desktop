import { BrowserApp } from '../browser_app.js';

export class SpeedtestApp extends BrowserApp {
  static NAME='speed'; static LABEL='Speed'; static ICON='speed';
  constructor(onExit){super(onExit,{title:'Speedtest',mode:'WEB'});this.rows=[];this.snapshot();}
  snapshot(){
    const c=navigator.connection;
    this.rows=[['Tip',c?.effectiveType||'n/a'],['Down',c?.downlink?`${c.downlink}Mb`:'n/a'],['RTT',c?.rtt?`${c.rtt}ms`:'n/a'],['Save',c?.saveData?'ON':'OFF']];
    this.status='Network API';
  }
  async onSel(){
    await this.task(async()=>{
      const bytes=512*1024; const url=`https://speed.cloudflare.com/__down?bytes=${bytes}&r=${Math.random()}`;
      const t0=performance.now(); const r=await fetch(url,{cache:'no-store'}); if(!r.ok) throw new Error(`HTTP ${r.status}`);
      const b=await r.arrayBuffer(); const sec=(performance.now()-t0)/1000; const mbps=(b.byteLength*8/sec/1e6).toFixed(1);
      this.rows=[['Down',`${mbps}Mb`],['Boyut',`${Math.round(b.byteLength/1024)}KB`],['Sure',`${sec.toFixed(2)}s`],['Kaynak','Cloudflare']];
      this.status='olculdu';
    },'olculuyor');
    if(this.lastError) this.snapshot();
  }
  draw(fb){this.drawHeader(fb,'WEB');this.drawRows(fb,this.rows);this.footer(fb,'SEL olc');}
}
