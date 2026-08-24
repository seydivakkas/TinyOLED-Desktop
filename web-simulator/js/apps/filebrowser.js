import { BrowserApp } from '../browser_app.js';

export class FileBrowserApp extends BrowserApp {
  static NAME='file'; static LABEL='Dosya'; static ICON='script';
  constructor(onExit){super(onExit,{title:'Dosya',mode:'WEB'});this.handle=null;this.entries=[];this.cursor=0;}
  async _pick(){
    if(!('showDirectoryPicker' in window)) throw new Error('File System Access API yok');
    this.handle=await window.showDirectoryPicker({mode:'read'});
    await this._list();
  }
  async _list(){
    const out=[]; for await(const [name,handle] of this.handle.entries())out.push({name,handle,kind:handle.kind});
    out.sort((a,b)=>a.kind===b.kind?a.name.localeCompare(b.name):a.kind==='directory'?-1:1);this.entries=out;this.cursor=0;
  }
  onUp(){if(this.entries.length)this.cursor=(this.cursor-1+this.entries.length)%this.entries.length;}
  onDown(){if(this.entries.length)this.cursor=(this.cursor+1)%this.entries.length;}
  async onSel(){
    await this.task(async()=>{
      if(!this.handle){await this._pick();return;}
      const e=this.entries[this.cursor];if(!e){await this._pick();return;}
      if(e.kind==='directory'){this.handle=e.handle;await this._list();}
      else{const f=await e.handle.getFile();this.status=`${Math.round(f.size/1024)}KB`;}
    },'dosya');
  }
  draw(fb){this.drawHeader(fb,'WEB');const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,this.entries.length-4)));const rows=this.entries.slice(start,start+4).map(e=>[e.kind==='directory'?'DIR':'FILE',e.name]);this.drawRows(fb,rows.length?rows:[['SEL','klasor sec']],this.cursor-start);this.footer(fb,this.handle?.name||'SEL klasor');}
}
