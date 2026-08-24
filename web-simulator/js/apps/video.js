import { BrowserApp, pickFile } from '../browser_app.js';

export class VideoPlayerApp extends BrowserApp {
  static NAME='video'; static LABEL='Video'; static ICON='video';
  constructor(onExit){
    super(onExit,{title:'Video 1-bit',mode:'WEB'});
    this.video=document.createElement('video');this.video.muted=true;this.video.playsInline=true;
    this.canvas=document.createElement('canvas');this.canvas.width=128;this.canvas.height=44;this.ctx=this.canvas.getContext('2d',{willReadFrequently:true});
    this.frame=null;this.name='--';
  }
  async onSel(){await this.task(async()=>{if(!this.video.src){const f=await pickFile('video/*');this.name=f.name;this.video.src=URL.createObjectURL(f);await this.video.play();this.status='PLAY';return;}if(this.video.paused){await this.video.play();this.status='PLAY';}else{this.video.pause();this.status='PAUSE';}},'video');}
  onUp(){this.video.currentTime=Math.min(this.video.duration||Infinity,this.video.currentTime+5);}
  onDown(){this.video.currentTime=Math.max(0,this.video.currentTime-5);}
  update(){super.update();if(!this.video.src||this.video.readyState<2)return;this.ctx.drawImage(this.video,0,0,128,44);this.frame=this.ctx.getImageData(0,0,128,44).data;}
  onLong(){this.video.pause();super.onLong();}
  draw(fb){this.drawHeader(fb,'WEB');if(this.frame){for(let y=0;y<44;y++)for(let x=0;x<128;x++){const i=(y*128+x)*4;const lum=.2126*this.frame[i]+.7152*this.frame[i+1]+.0722*this.frame[i+2];if(lum>128)fb.pixel(x,20+y);}}else fb.textCentered('SEL video sec',34);this.footer(fb,`${this.video.paused?'PAUSE':'PLAY'} ${Math.floor(this.video.currentTime||0)}s`);}
}
