import { BrowserApp } from '../browser_app.js';
import { bridgeJSON, configureBridge } from '../browser_bridge.js';

export class PowerApp extends BrowserApp {
  static NAME='power'; static LABEL='Guc'; static ICON='service';
  constructor(onExit){super(onExit,{title:'Guc',mode:'WEB/BRG'});this.actions=['WakeLock','Pi reboot','Pi shutdown'];this.cursor=0;this.battery=null;this.wake=null;this._battery();}
  async _battery(){if(navigator.getBattery)this.battery=await navigator.getBattery().catch(()=>null);}
  onUp(){this.cursor=(this.cursor-1+this.actions.length)%this.actions.length;}
  onDown(){this.cursor=(this.cursor+1)%this.actions.length;}
  async onSel(){
    const action=this.actions[this.cursor];
    await this.task(async()=>{
      if(action==='WakeLock'){
        if(this.wake){await this.wake.release();this.wake=null;}else{if(!navigator.wakeLock)throw new Error('Wake Lock yok');this.wake=await navigator.wakeLock.request('screen');}
      } else {
        if(!confirm(`${action} komutunu yerel TinyOLED bridge'e gonder?`)) return;
        configureBridge();
        await bridgeJSON('/api/power',{method:'POST',body:{action:action==='Pi reboot'?'reboot':'shutdown'}});
      }
    },action);
  }
  draw(fb){this.drawHeader(fb,'WEB');this.drawRows(fb,[['Pil',this.battery?`${Math.round(this.battery.level*100)}%`:'n/a'],['Wake',this.wake?'ON':'OFF'],['Eylem',this.actions[this.cursor]],['Bridge','local']]);this.footer(fb,'UP/DN sec SEL uygula');}
}
