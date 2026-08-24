import { BrowserApp, clamp } from '../browser_app.js';

const SETS=[
  ['A-z0-9','ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'],
  ['Guclu','ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*_-+='],
  ['PIN','0123456789']
];
function randomString(chars,len){
  const out=[]; const limit=256-(256%chars.length); const buf=new Uint8Array(Math.max(32,len*2));
  while(out.length<len){ crypto.getRandomValues(buf); for(const b of buf){ if(b<limit) out.push(chars[b%chars.length]); if(out.length===len) break; } }
  return out.join('');
}
export class PasswordGeneratorApp extends BrowserApp {
  static NAME='passgen'; static LABEL='Sifre'; static ICON='passkey';
  constructor(onExit){super(onExit,{title:'Sifre Uret',mode:'WEB'});this.length=16;this.setIndex=1;this.password='';this.generate();}
  generate(){this.password=randomString(SETS[this.setIndex][1],this.length);this.status='crypto RNG';}
  onUp(){this.length=clamp(this.length+2,6,32);this.generate();}
  onDown(){this.length=clamp(this.length-2,6,32);this.generate();}
  onSel(){this.setIndex=(this.setIndex+1)%SETS.length;this.generate(); navigator.clipboard?.writeText(this.password).catch(()=>{});}
  draw(fb){
    this.drawHeader(fb,'WEB');
    this.drawRows(fb,[['Uzun',this.length],['Set',SETS[this.setIndex][0]],['Parola',this.password.slice(0,10)],['Kaynak','WebCrypto']],-1);
    this.footer(fb,'UP/DN len SEL set+copy');
  }
}
