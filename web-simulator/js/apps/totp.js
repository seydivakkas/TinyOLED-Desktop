import { BrowserApp } from '../browser_app.js';

const B32='ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
function base32Decode(input){
  const clean=input.toUpperCase().replace(/[^A-Z2-7]/g,'');
  let bits='', out=[];
  for(const ch of clean){ const v=B32.indexOf(ch); if(v<0) continue; bits+=v.toString(2).padStart(5,'0'); }
  for(let i=0;i+8<=bits.length;i+=8) out.push(parseInt(bits.slice(i,i+8),2));
  return new Uint8Array(out);
}
async function hotp(secret,counter){
  const key=await crypto.subtle.importKey('raw',base32Decode(secret),{name:'HMAC',hash:'SHA-1'},false,['sign']);
  const buf=new ArrayBuffer(8); const view=new DataView(buf);
  view.setUint32(0,Math.floor(counter/0x100000000)); view.setUint32(4,counter>>>0);
  const sig=new Uint8Array(await crypto.subtle.sign('HMAC',key,buf));
  const off=sig[sig.length-1]&0x0f;
  const bin=((sig[off]&0x7f)<<24)|(sig[off+1]<<16)|(sig[off+2]<<8)|sig[off+3];
  return String(bin%1000000).padStart(6,'0');
}
export class TOTPApp extends BrowserApp {
  static NAME='totp'; static LABEL='TOTP'; static ICON='key';
  constructor(onExit){ super(onExit,{title:'TOTP RFC6238',mode:'WEB'}); this.secret=sessionStorage.getItem('tinyoled.totp.secret')||''; this.code='------'; this.remain=30; }
  async onSel(){
    const next=prompt('Base32 TOTP secret (yalnizca sessionStorage)',this.secret);
    if(next){ this.secret=next.trim(); sessionStorage.setItem('tinyoled.totp.secret',this.secret); await this._refresh(); }
  }
  async _refresh(){
    if(!this.secret){this.code='------'; return;}
    try{ const step=Math.floor(Date.now()/1000/30); this.code=await hotp(this.secret,step); this.status='RFC6238'; }
    catch(e){this.code='HATA'; this.status='secret hatali';}
  }
  update(){super.update(); this.remain=30-(Math.floor(Date.now()/1000)%30); if(this._tick%10===0) this._refresh();}
  draw(fb){
    this.drawHeader(fb,'WEB');
    fb.textCentered(this.code,26);
    fb.textCentered(`Kalan ${this.remain}s`,38);
    fb.progressBar(14,48,100,5,this.remain,30);
    this.footer(fb,'SEL secret');
  }
}
