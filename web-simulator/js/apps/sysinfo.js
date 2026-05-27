/** TinyOLED Desktop — System Info (Simulated Data) */
import { Font } from '../font.js';
const CONTENT_Y = 10, LINE_H = 9;

export class SysInfoApp {
  static NAME='sysinfo'; static LABEL='Sistem'; static ICON='cpu';
  constructor(onExit) {
    this.onExit=onExit; this._page=0; this._tick=0;
    this.PAGES=['cpu_ram','temp_disk','network','uptime'];
    this._startTime = performance.now();
  }
  onUp()   { this._page=(this._page-1+this.PAGES.length)%this.PAGES.length; }
  onDown() { this._page=(this._page+1)%this.PAGES.length; }
  onSel()  { this.onExit(); }
  onLong() { this.onExit(); }
  update() { this._tick++; }

  draw(fb) {
    const p = this.PAGES[this._page];
    if (p==='cpu_ram') this._cpuRam(fb);
    else if (p==='temp_disk') this._tempDisk(fb);
    else if (p==='network') this._network(fb);
    else this._uptime(fb);
    // Page dots
    for (let i=0;i<this.PAGES.length;i++) {
      const px = 64 - this.PAGES.length*3 + i*6;
      fb.rect(px, 58, 4, 3, true, i===this._page);
    }
  }

  _cpuRam(fb) {
    fb.icon('cpu',1,CONTENT_Y); fb.text('CPU & RAM',12,CONTENT_Y);
    let y=CONTENT_Y+10;
    const cpu=Math.floor(40+25*Math.sin(this._tick*0.15));
    fb.text(`CPU: ${String(cpu).padStart(3)}%`,1,y);
    fb.progressBar(50,y,76,7,cpu); y+=LINE_H+1;
    const mu=380+Math.floor(50*Math.sin(this._tick*0.08)), mt=512, mp=Math.floor(100*mu/mt);
    fb.text(`RAM: ${mu}/${mt}MB`,1,y); y+=LINE_H;
    fb.progressBar(1,y,126,7,mp);
  }

  _tempDisk(fb) {
    fb.icon('temp',1,CONTENT_Y); fb.text('Isi & Disk',12,CONTENT_Y);
    let y=CONTENT_Y+10;
    const temp=45+Math.floor(7*Math.sin(this._tick*0.1));
    fb.text(`Sicak: ${temp}C${temp>70?' !!':''}`,1,y); y+=LINE_H;
    fb.progressBar(1,y,126,7,temp,90); y+=LINE_H+1;
    fb.icon('folder',1,y); fb.text('12G/32G (38%)',12,y+1);
  }

  _network(fb) {
    fb.icon('wifi',1,CONTENT_Y); fb.text('Ag',12,CONTENT_Y);
    let y=CONTENT_Y+10;
    fb.text('RX: 142 MB',1,y); y+=LINE_H;
    fb.text('TX: 28 MB',1,y); y+=LINE_H;
    fb.text('192.168.1.42',1,y);
  }

  _uptime(fb) {
    fb.icon('heart',1,CONTENT_Y); fb.text('Uptime',12,CONTENT_Y);
    let y=CONTENT_Y+12;
    const secs=Math.floor((performance.now()-this._startTime)/1000);
    const h=Math.floor(secs/3600), m=Math.floor((secs%3600)/60), s=secs%60;
    fb.textCentered(`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`,y);
    y+=LINE_H+4; fb.text('Host: tinyoled-pi',1,y);
    y+=LINE_H; fb.text('6.1.21-v8+',1,y);
  }
}
