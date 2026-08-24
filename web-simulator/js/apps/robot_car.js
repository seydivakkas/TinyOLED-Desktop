import { BrowserApp } from '../browser_app.js';
import { ioCommand } from '../browser_bridge.js';
const DIRS=['stop','forward','left','right','back'];
export class RobotCarApp extends BrowserApp {
  static NAME='car'; static LABEL='Araba'; static ICON='car';
  constructor(onExit){super(onExit,{title:'Robot Araba',mode:'SER/BRG'});this.cursor=0;this.speed=50;this.last='stop';}
  onUp(){this.cursor=(this.cursor-1+DIRS.length)%DIRS.length;}
  onDown(){this.cursor=(this.cursor+1)%DIRS.length;}
  async onSel(){await this.task(async()=>{const dir=DIRS[this.cursor];await ioCommand({cmd:'car.drive',direction:dir,speed:this.speed});this.last=dir;this.status='gonderildi';},'motor');}
  onLong(){ioCommand({cmd:'car.drive',direction:'stop',speed:0}).catch(()=>{});super.onLong();}
  draw(fb){this.drawHeader(fb,'SER');this.drawRows(fb,[['Sec',DIRS[this.cursor]],['Son',this.last],['Hiz',`${this.speed}%`],['Surucu','L298N']]);this.footer(fb,'UP/DN yon SEL send');}
}
