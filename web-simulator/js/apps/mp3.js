import { BrowserApp, pickFile } from '../browser_app.js';

export class MP3PlayerApp extends BrowserApp {
  static NAME='mp3'; static LABEL='MP3'; static ICON='music';
  constructor(onExit){super(onExit,{title:'MP3 Calar',mode:'WEB'});this.audio=new Audio();this.fileName='--';this.duration=0;this.audio.addEventListener('loadedmetadata',()=>{this.duration=this.audio.duration||0;});}
  async _pick(){const f=await pickFile('audio/*');this.fileName=f.name;this.audio.src=URL.createObjectURL(f);await this.audio.play();this.status='PLAY';}
  async onSel(){await this.task(async()=>{if(!this.audio.src){await this._pick();return;}if(this.audio.paused){await this.audio.play();this.status='PLAY';}else{this.audio.pause();this.status='PAUSE';}},'audio');}
  onUp(){if(this.audio.src)this.audio.currentTime=Math.min(this.duration||Infinity,this.audio.currentTime+10);}
  onDown(){if(this.audio.src)this.audio.currentTime=Math.max(0,this.audio.currentTime-10);}
  onLong(){this.audio.pause();super.onLong();}
  draw(fb){this.drawHeader(fb,'WEB');const t=this.audio.currentTime||0,d=this.duration||0;this.drawRows(fb,[['Dosya',this.fileName],['Durum',this.audio.paused?'PAUSE':'PLAY'],['Sure',`${Math.floor(t)}/${Math.floor(d)}s`],['Seek','UP/DN 10s']]);this.footer(fb,'SEL sec/play');}
}
