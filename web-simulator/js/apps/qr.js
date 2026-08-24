import { BrowserApp } from '../browser_app.js';

export class QRCodeApp extends BrowserApp {
  static NAME='qr'; static LABEL='QR'; static ICON='qr';
  constructor(onExit){super(onExit,{title:'QR Kod',mode:'WEB'});this.text=localStorage.getItem('tinyoled.qr.text')||location.href;this.modules=null;this.make();}
  async make(){
    await this.task(async()=>{
      const mod=await import('https://cdn.jsdelivr.net/npm/qrcode@1.5.4/+esm');
      const qr=mod.default?.create ? mod.default.create(this.text,{errorCorrectionLevel:'M'}) : mod.create(this.text,{errorCorrectionLevel:'M'});
      this.modules=qr.modules; this.status=`v${qr.version}`;
    },'QR uretiliyor');
  }
  onSel(){const t=prompt('QR icerigi',this.text);if(t){this.text=t;localStorage.setItem('tinyoled.qr.text',t);this.make();}}
  draw(fb){
    this.drawHeader(fb,'WEB');
    if(!this.modules){fb.textCentered('QR yukleniyor',31);this.footer(fb);return;}
    const size=this.modules.size, scale=Math.max(1,Math.floor(44/size)), ox=Math.floor((128-size*scale)/2), oy=20;
    for(let y=0;y<size;y++)for(let x=0;x<size;x++)if(this.modules.get(y,x))fb.rect(ox+x*scale,oy+y*scale,scale,scale,true,true);
    this.footer(fb,'SEL icerik');
  }
}
