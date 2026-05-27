/** TinyOLED Desktop — Settings App */
export class SettingsApp {
  static NAME='settings'; static LABEL='Ayar'; static ICON='gear';
  constructor(onExit,notify) {
    this.onExit=onExit; this.notify=notify||(()=>{});
    this.items=['Parlaklik','Kontrast','FPS','Ekran Rengi','Hakkinda'];
    this.values=[200,2,20,0,0];
    this.cursor=0;
  }
  onUp()   { this.cursor=(this.cursor-1+this.items.length)%this.items.length; }
  onDown() { this.cursor=(this.cursor+1)%this.items.length; }
  onSel()  {
    if(this.cursor===0) { this.values[0]=this.values[0]>=250?50:this.values[0]+50; this.notify(`Parlaklik: ${this.values[0]}`); }
    else if(this.cursor===1) { this.values[1]=(this.values[1]+1)%4; }
    else if(this.cursor===2) { this.values[2]=this.values[2]>=30?10:this.values[2]+5; }
    else if(this.cursor===3) { this.values[3]=(this.values[3]+1)%3; }
  }
  onLong() { this.onExit(); }
  update() {}
  draw(fb) {
    fb.icon('gear',1,10); fb.text('Ayarlar',12,10); fb.hline(0,18,128);
    const labels=['Parlk','Kont','FPS','Renk','Info'];
    const vals=[
      String(this.values[0]),
      String(this.values[1]),
      `${this.values[2]}fps`,
      ['Cyan','Yesil','Beyaz'][this.values[3]],
      'v1.0'
    ];
    for(let i=0;i<this.items.length&&i<5;i++) {
      const y=20+i*8, sel=(i===this.cursor);
      if(sel) fb.rect(0,y-1,128,9,true,true);
      fb.text(`${labels[i]}: ${vals[i]}`,4,y,!sel);
    }
    fb.text('[LONG] Geri',2,56);
  }
}
