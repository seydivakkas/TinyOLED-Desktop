import { BrowserApp, clamp } from '../browser_app.js';
import { ioCommand } from '../browser_bridge.js';
export class ServoControlApp extends BrowserApp {
  static NAME='servo'; static LABEL='Servo'; static ICON='servo';
  constructor(onExit){super(onExit,{title:'Servo',mode:'SER/BRG'});this.angle=90;this.sent='--';}
  onUp(){this.angle=clamp(this.angle+5,0,180);}
  onDown(){this.angle=clamp(this.angle-5,0,180);}
  async onSel(){await this.task(async()=>{const d=await ioCommand({cmd:'servo.write',pin:18,angle:this.angle});this.sent=d.angle??this.angle;this.status='gonderildi';},'servo');}
  draw(fb){this.drawHeader(fb,'SER');this.drawRows(fb,[['Aci',`${this.angle}deg`],['GPIO','18 PWM'],['Son',`${this.sent}deg`],['Proto','JSON']]);this.footer(fb,'UP/DN aci SEL send');}
}
