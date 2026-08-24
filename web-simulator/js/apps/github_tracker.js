import { BrowserApp } from '../browser_app.js';

export class GitHubTrackerApp extends BrowserApp {
  static NAME='github'; static LABEL='GitHub'; static ICON='github';
  constructor(onExit){super(onExit,{title:'GitHub',mode:'NET'});this.user=localStorage.getItem('tinyoled.github.user')||'seydivakkas';this.rows=[];this.refresh();}
  async refresh(){
    await this.task(async()=>{
      const [u,e]=await Promise.all([
        fetch(`https://api.github.com/users/${encodeURIComponent(this.user)}`),
        fetch(`https://api.github.com/users/${encodeURIComponent(this.user)}/events/public?per_page=30`)
      ]);
      if(!u.ok) throw new Error(`GitHub ${u.status}`);
      const user=await u.json(); const events=e.ok?await e.json():[];
      const pushes=events.filter(x=>x.type==='PushEvent').length;
      const commits=events.filter(x=>x.type==='PushEvent').reduce((n,x)=>n+(x.payload?.commits?.length||0),0);
      this.rows=[['Kullanici',this.user],['Repo',user.public_repos],['Push',pushes],['Commit',commits]];
      this.status='canli';
    },'GitHub');
  }
  onUp(){const u=prompt('GitHub username',this.user);if(u){this.user=u.trim();localStorage.setItem('tinyoled.github.user',this.user);this.refresh();}}
  onSel(){this.refresh();}
  draw(fb){this.drawHeader(fb,'NET');this.drawRows(fb,this.rows.length?this.rows:[['User',this.user],['Durum','bekle']]);this.footer(fb,'UP user SEL yenile');}
}
