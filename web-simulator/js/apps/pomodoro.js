/** TinyOLED Desktop — Pomodoro Timer */
export class PomodoroApp {
  static NAME='pomodoro'; static LABEL='Pomo'; static ICON='timer';
  static WORK=25*60; static BREAK=5*60;
  constructor(onExit,notify) {
    this.onExit=onExit; this.notify=notify||(()=>{});
    this.running=false; this.working=true;
    this.remaining=PomodoroApp.WORK; this.sessions=0; this._last=0;
  }
  onUp(){} onDown(){}
  onSel() {
    if(!this.running){this.running=true;this._last=performance.now()/1000;}
    else this.running=false;
  }
  onLong(){this.onExit();}
  update() {
    if(!this.running) return;
    const now=performance.now()/1000, dt=now-this._last; this._last=now;
    this.remaining-=dt;
    if(this.remaining<=0) {
      if(this.working){this.sessions++;this.notify(`Mola! (${this.sessions})`);this.remaining=PomodoroApp.BREAK;}
      else{this.notify('Calismaya basla!');this.remaining=PomodoroApp.WORK;}
      this.working=!this.working;
    }
  }
  draw(fb) {
    fb.icon('timer',1,10); fb.text('Pomodoro',12,10); fb.hline(0,18,128);
    const mins=Math.floor(this.remaining/60), secs=Math.floor(this.remaining%60);
    fb.textCentered(`${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`,30);
    const total=this.working?PomodoroApp.WORK:PomodoroApp.BREAK;
    fb.progressBar(10,42,108,6,total-this.remaining,total);
    fb.text(this.working?'CALISMA':'MOLA',2,52);
    fb.text(`#${this.sessions}`,60,52);
    fb.text(this.running?'DUR':'BASLA',90,52);
  }
}
