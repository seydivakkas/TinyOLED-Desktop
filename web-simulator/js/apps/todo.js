import { BrowserApp, loadJSON, saveJSON } from '../browser_app.js';
const KEY='tinyoled.todo.v1';

export class TodoApp extends BrowserApp {
  static NAME='todo'; static LABEL='Todo'; static ICON='todo';
  constructor(onExit){
    super(onExit,{title:'Gorevler',mode:'WEB'});
    this.tasks=loadJSON(KEY,[{text:'TinyOLED test',done:false}]);
    this.cursor=0;
  }
  get count(){ return this.tasks.length + 1; }
  onUp(){ this.cursor=(this.cursor-1+this.count)%this.count; }
  onDown(){ this.cursor=(this.cursor+1)%this.count; }
  onSel(){
    if(this.cursor===this.tasks.length){ this._add(); return; }
    this.tasks[this.cursor].done=!this.tasks[this.cursor].done;
    saveJSON(KEY,this.tasks); this.status='toggle';
  }
  _add(){
    const t=prompt('Yeni gorev');
    if(t?.trim()){
      this.tasks.push({text:t.trim(),done:false});
      saveJSON(KEY,this.tasks);
      this.cursor=this.tasks.length-1;
      this.status='eklendi';
    }
  }
  draw(fb){
    this.drawHeader(fb,'WEB');
    const entries=[...this.tasks.map(t=>({label:t.done?'[x]':'[ ]',value:t.text})),{label:'[+]',value:'Yeni gorev'}];
    const start=Math.max(0,Math.min(this.cursor-1,Math.max(0,entries.length-4)));
    const rows=entries.slice(start,start+4).map(e=>[e.label,e.value]);
    this.drawRows(fb,rows,this.cursor-start);
    this.footer(fb,'SEL toggle/ekle');
  }
}
