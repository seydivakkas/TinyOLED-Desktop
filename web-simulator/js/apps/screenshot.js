import { BrowserApp, downloadBlob } from '../browser_app.js';

export class ScreenshotApp extends BrowserApp {
  static NAME='shot'; static LABEL='Shot'; static ICON='camera';
  constructor(onExit){super(onExit,{title:'Screenshot',mode:'WEB'});this.count=0;}
  onSel(){
    const canvas=document.getElementById('oled-canvas');
    if(!canvas){this.status='canvas yok';return;}
    canvas.toBlob(blob=>{if(!blob){this.status='PNG hata';return;}this.count++;downloadBlob(blob,`tinyoled-${new Date().toISOString().replace(/[:.]/g,'-')}.png`);this.status='indirildi';},'image/png');
  }
  draw(fb){this.drawHeader(fb,'WEB');this.drawRows(fb,[['Kaynak','OLED canvas'],['Format','PNG'],['Boyut','640x320'],['Kayit',this.count]]);this.footer(fb,'SEL indir');}
}
