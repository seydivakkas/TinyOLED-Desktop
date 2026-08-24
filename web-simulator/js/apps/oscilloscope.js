import { BrowserApp } from '../browser_app.js';
export class OscilloscopeApp extends BrowserApp {
  static NAME='scope'; static LABEL='Scope'; static ICON='scope';
  constructor(onExit){super(onExit,{title:'Osiloskop',mode:'WEB'});this.stream=null;this.ctx=null;this.analyser=null;this.data=new Uint8Array(128);}
  async onSel(){
    await this.task(async()=>{
      if(this.stream){this.stream.getTracks().forEach(t=>t.stop());this.stream=null;this.status='durdu';return;}
      this.stream=await navigator.mediaDevices.getUserMedia({audio:true,video:false});
      this.ctx=new AudioContext();const src=this.ctx.createMediaStreamSource(this.stream);this.analyser=this.ctx.createAnalyser();this.analyser.fftSize=256;src.connect(this.analyser);this.data=new Uint8Array(this.analyser.frequencyBinCount);this.status='mikrofon';
    },'mic izin');
  }
  update(){super.update();if(this.analyser)this.analyser.getByteTimeDomainData(this.data);}
  onLong(){this.stream?.getTracks().forEach(t=>t.stop());this.ctx?.close();super.onLong();}
  draw(fb){this.drawHeader(fb,'WEB');fb.rect(2,22,124,30);if(this.data?.length){for(let i=1;i<Math.min(124,this.data.length);i++){const y0=37+Math.round((this.data[i-1]-128)/8),y1=37+Math.round((this.data[i]-128)/8);fb.line(i+1,y0,i+2,y1);}}this.footer(fb,'SEL mic start/stop');}
}
