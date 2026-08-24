import { BrowserApp } from '../browser_app.js';

export class IPCameraApp extends BrowserApp {
  static NAME='ipcam'; static LABEL='IPCam'; static ICON='camera';
  constructor(onExit){
    super(onExit,{title:'Kamera',mode:'WEB'});
    this.stream=null;this.video=document.createElement('video');this.video.playsInline=true;this.video.muted=true;
    this.canvas=document.createElement('canvas');this.canvas.width=128;this.canvas.height=44;this.ctx=this.canvas.getContext('2d',{willReadFrequently:true});this.frame=null;
  }
  async onSel(){await this.task(async()=>{if(this.stream){this.stream.getTracks().forEach(t=>t.stop());this.stream=null;this.frame=null;this.status='kapali';return;}this.stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:'environment'},audio:false});this.video.srcObject=this.stream;await this.video.play();this.status='canli';},'kamera izin');}
  update(){super.update();if(!this.stream||this.video.readyState<2)return;this.ctx.drawImage(this.video,0,0,128,44);this.frame=this.ctx.getImageData(0,0,128,44).data;}
  onLong(){this.stream?.getTracks().forEach(t=>t.stop());super.onLong();}
  draw(fb){this.drawHeader(fb,'WEB');if(this.frame){for(let y=0;y<44;y++)for(let x=0;x<128;x++){const i=(y*128+x)*4;const lum=(this.frame[i]+this.frame[i+1]+this.frame[i+2])/3;const threshold=96+((x+y)&1)*48;if(lum>threshold)fb.pixel(x,20+y);}}else fb.textCentered('SEL kamera ac',34);this.footer(fb,this.stream?'SEL kapat':'SEL baslat');}
}
