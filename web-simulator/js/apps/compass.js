import { BrowserApp } from '../browser_app.js';
import { ioCommand } from '../browser_bridge.js';
export class CompassApp extends BrowserApp {
  static NAME='compass'; static LABEL='Pusula'; static ICON='compass';
  constructor(onExit){super(onExit,{title:'Pusula',mode:'WEB/SER'});this.heading=null;this.source='none';this._listener=e=>{let h=e.webkitCompassHeading;if(h==null&&e.alpha!=null)h=(360-e.alpha)%360;if(h!=null){this.heading=h;this.source='device';}};}
  async _enableDevice(){
    if(typeof DeviceOrientationEvent==='undefined')throw new Error('Orientation API yok');
    if(typeof DeviceOrientationEvent.requestPermission==='function'){const p=await DeviceOrientationEvent.requestPermission();if(p!=='granted')throw new Error('izin yok');}
    window.addEventListener('deviceorientation',this._listener,true);this.status='device';
  }
  async onSel(){await this.task(async()=>{try{await this._enableDevice();}catch{const d=await ioCommand({cmd:'compass.read'});this.heading=d.heading;this.source='HMC5883L';}},'pusula');}
  onLong(){window.removeEventListener('deviceorientation',this._listener,true);super.onLong();}
  draw(fb){this.drawHeader(fb,'WEB');const h=this.heading==null?'--':`${Math.round(this.heading)}deg`;const dir=this.heading==null?'--':['K','KD','D','GD','G','GB','B','KB'][Math.round(this.heading/45)%8];this.drawRows(fb,[['Aci',h],['Yon',dir],['Kaynak',this.source],['SEL','izin/bridge']]);this.footer(fb,'SEL baslat');}
}
