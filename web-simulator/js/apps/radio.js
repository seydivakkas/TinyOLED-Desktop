import { BrowserApp } from '../browser_app.js';

const STATIONS=[
  ['Groove','https://ice2.somafm.com/groovesalad-128-mp3'],
  ['Drone','https://ice2.somafm.com/dronezone-128-mp3'],
  ['Secret','https://ice2.somafm.com/secretagent-128-mp3']
];
export class RadioApp extends BrowserApp {
  static NAME='radio'; static LABEL='Radyo'; static ICON='radio';
  constructor(onExit){super(onExit,{title:'Internet Radio',mode:'NET'});this.audio=new Audio();this.audio.crossOrigin='anonymous';this.cursor=0;this.playing=false;}
  onUp(){this.cursor=(this.cursor-1+STATIONS.length)%STATIONS.length;if(this.playing)this._load();}
  onDown(){this.cursor=(this.cursor+1)%STATIONS.length;if(this.playing)this._load();}
  async _load(){this.audio.src=STATIONS[this.cursor][1];await this.audio.play();this.playing=true;this.status='stream';}
  async onSel(){await this.task(async()=>{if(this.playing){this.audio.pause();this.playing=false;this.status='pause';}else await this._load();},'radio');}
  onLong(){this.audio.pause();super.onLong();}
  draw(fb){this.drawHeader(fb,'NET');this.drawRows(fb,[['Kanal',STATIONS[this.cursor][0]],['Durum',this.playing?'PLAY':'STOP'],['Codec','MP3'],['Kaynak','SomaFM']]);this.footer(fb,'UP/DN kanal SEL play');}
}
