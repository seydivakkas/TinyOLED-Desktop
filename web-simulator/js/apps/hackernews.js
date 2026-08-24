import { BrowserApp } from '../browser_app.js';

export class HackerNewsApp extends BrowserApp {
  static NAME='news'; static LABEL='HNews'; static ICON='news';
  constructor(onExit){super(onExit,{title:'HackerNews',mode:'NET'});this.items=[];this.cursor=0;this.refresh();}
  async refresh(){
    await this.task(async()=>{
      const ids=await (await fetch('https://hacker-news.firebaseio.com/v0/topstories.json')).json();
      const top=ids.slice(0,8);
      const stories=await Promise.all(top.map(id=>fetch(`https://hacker-news.firebaseio.com/v0/item/${id}.json`).then(r=>r.json())));
      this.setItems(stories.map(s=>({label:String(s.score||0),value:s.title||'',url:s.url||`https://news.ycombinator.com/item?id=${s.id}`})));
      this.status='canli';
    },'HN');
  }
  onSel(){const s=this.selected();if(s?.url)window.open(s.url,'_blank','noopener');}
  draw(fb){
    this.drawHeader(fb,'NET');
    const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,this.items.length-4)));
    this.drawRows(fb,this.items.slice(start,start+4).map(x=>[x.label,x.value.slice(0,11)]),this.cursor-start);
    this.footer(fb,'SEL ac');
  }
}
