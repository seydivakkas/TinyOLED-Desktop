import { BrowserApp } from '../browser_app.js';

export class VoiceControlApp extends BrowserApp {
  static NAME='voice'; static LABEL='Ses'; static ICON='mic';
  constructor(onExit){super(onExit,{title:'Sesli Kontrol',mode:'WEB'});this.text='--';this.conf=0;this.recognition=null;}
  async onSel(){
    const R=window.SpeechRecognition||window.webkitSpeechRecognition;
    if(!R){this.status='Speech API yok';return;}
    if(!this.recognition){
      this.recognition=new R();this.recognition.lang='tr-TR';this.recognition.interimResults=true;this.recognition.continuous=false;
      this.recognition.onresult=e=>{const r=e.results[e.results.length-1][0];this.text=r.transcript;this.conf=r.confidence||0;this.status=e.results[e.results.length-1].isFinal?'tamam':'dinliyor';};
      this.recognition.onerror=e=>{this.status=e.error||'hata';};
      this.recognition.onend=()=>{if(this.status==='dinliyor')this.status='bitti';};
    }
    this.status='dinliyor';this.recognition.start();
  }
  onLong(){try{this.recognition?.stop();}catch{}super.onLong();}
  draw(fb){this.drawHeader(fb,'WEB');this.drawRows(fb,[['Metin',this.text.slice(0,11)],['Guven',this.conf?`${Math.round(this.conf*100)}%`:'--'],['Dil','tr-TR'],['Motor','Speech API']]);this.footer(fb,'SEL dinle');}
}
