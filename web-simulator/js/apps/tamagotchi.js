import { BrowserApp, clamp, loadJSON, saveJSON } from '../browser_app.js';

const KEY = 'tinyoled.tamagotchi.v1';
const defaultState = () => ({ hunger: 78, happy: 82, energy: 76, clean: 88, updated: Date.now() });

export class TamagotchiApp extends BrowserApp {
  static NAME='tamagotchi'; static LABEL='Pet'; static ICON='pet';
  constructor(onExit) {
    super(onExit, { title: 'Tamagotchi', mode: 'WEB' });
    this.state = loadJSON(KEY, defaultState());
    this.actions = ['Besle', 'Oyna', 'Uyut', 'Temizle'];
    this.cursor = 0;
    this._applyDecay();
  }
  _applyDecay() {
    const now = Date.now();
    const hours = Math.max(0, (now - (this.state.updated || now)) / 3600000);
    this.state.hunger = clamp(this.state.hunger - hours * 5, 0, 100);
    this.state.happy = clamp(this.state.happy - hours * 3, 0, 100);
    this.state.energy = clamp(this.state.energy - hours * 2.5, 0, 100);
    this.state.clean = clamp(this.state.clean - hours * 2, 0, 100);
    this.state.updated = now;
    saveJSON(KEY, this.state);
  }
  onUp(){ this.cursor=(this.cursor-1+this.actions.length)%this.actions.length; }
  onDown(){ this.cursor=(this.cursor+1)%this.actions.length; }
  onSel(){
    const a=this.actions[this.cursor];
    if(a==='Besle') this.state.hunger=clamp(this.state.hunger+24,0,100);
    if(a==='Oyna'){ this.state.happy=clamp(this.state.happy+22,0,100); this.state.energy=clamp(this.state.energy-8,0,100); }
    if(a==='Uyut') this.state.energy=clamp(this.state.energy+30,0,100);
    if(a==='Temizle') this.state.clean=100;
    this.state.updated=Date.now(); saveJSON(KEY,this.state); this.status=a;
  }
  update(){ super.update(); if(this._tick%1200===0) this._applyDecay(); }
  draw(fb){
    this.drawHeader(fb,'WEB');
    const rows=[['Aclik',`${Math.round(this.state.hunger)}%`],['Mutlu',`${Math.round(this.state.happy)}%`],['Enerji',`${Math.round(this.state.energy)}%`],['Temiz',`${Math.round(this.state.clean)}%`]];
    this.drawRows(fb,rows,-1);
    fb.text(this.actions[this.cursor].slice(0,18),2,56);
  }
}
