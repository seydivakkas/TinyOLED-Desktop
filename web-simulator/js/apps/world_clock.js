import { BrowserApp } from '../browser_app.js';
const ZONES=[['IST','Europe/Istanbul'],['LON','Europe/London'],['NYC','America/New_York'],['TYO','Asia/Tokyo'],['SYD','Australia/Sydney']];

export class WorldClockApp extends BrowserApp {
  static NAME='world'; static LABEL='Dunya'; static ICON='world';
  constructor(onExit){super(onExit,{title:'Dunya Saati',mode:'WEB'});this.offset=0;}
  onUp(){this.offset=(this.offset-1+ZONES.length)%ZONES.length;}
  onDown(){this.offset=(this.offset+1)%ZONES.length;}
  onSel(){this.offset=0;}
  draw(fb){
    this.drawHeader(fb,'WEB'); const now=new Date();
    const ordered=[...ZONES.slice(this.offset),...ZONES.slice(0,this.offset)].slice(0,4);
    const rows=ordered.map(([n,z])=>[n,new Intl.DateTimeFormat('tr-TR',{timeZone:z,hour:'2-digit',minute:'2-digit',hour12:false}).format(now)]);
    this.drawRows(fb,rows);this.footer(fb,'UP/DN sehir');
  }
}
