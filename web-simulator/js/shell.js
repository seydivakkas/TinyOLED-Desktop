/**
 * TinyOLED Desktop — Desktop Shell (57-app browser catalog)
 * State machine: SPLASH -> HOME -> APP
 */
import { Framebuffer } from './framebuffer.js';
import { OLEDDisplay } from './display.js';
import { InputManager, EVT_UP, EVT_DOWN, EVT_SEL, EVT_LONG } from './input.js';
import { Scheduler } from './scheduler.js';
import { StatusBar } from './statusbar.js';
import { Launcher } from './launcher.js';
import { NotificationManager } from './notification.js';

import { ClockApp } from './apps/clock.js';
import { SysInfoApp } from './apps/sysinfo.js';
import { SettingsApp } from './apps/settings.js';
import { SnakeApp } from './apps/snake.js';
import { FlappyApp } from './apps/flappy.js';
import { DiceApp } from './apps/dice.js';
import { StarfieldApp } from './apps/starfield.js';
import { GameOfLifeApp } from './apps/gameoflife.js';
import { DVDLogoApp } from './apps/dvd.js';
import { MatrixRainApp } from './apps/matrix.js';
import { Cube3DApp } from './apps/cube3d.js';
import { FractalApp } from './apps/fractal.js';
import { MoonApp } from './apps/moon.js';
import { PomodoroApp } from './apps/pomodoro.js';
import { BreathingApp } from './apps/breathing.js';
import {
  WiFiApp, FileBrowserApp, PowerApp, TamagotchiApp, GraphApp, DockerApp, SystemdApp,
  GPIOViewerApp, I2CScannerApp, CommandRunnerApp, OscilloscopeApp, MultimeterApp,
  SSHAlertApp, TOTPApp, PasswordGeneratorApp, WiFiScannerApp, CryptoTickerApp,
  QRCodeApp, GitHubTrackerApp, SpeedtestApp, HackerNewsApp, TemperatureHumidityApp,
  UPSBatteryApp, PlantMonitorApp, CompassApp, MP3PlayerApp, RadioApp, VideoPlayerApp,
  TelegramApp, EmailApp, WorldClockApp, PixelArtApp, ScreenshotApp, HIITTimerApp,
  ServoControlApp, RobotCarApp, PiHoleApp, IPCameraApp, VoiceControlApp, SDHealthApp,
  APTUpdateApp, TodoApp
} from './apps/extended_apps.js';

const State = { SPLASH: 0, HOME: 1, APP: 2 };
const SPLASH_FRAMES = 40;
const TARGET_FPS = 20;

export class Desktop {
  constructor(canvas) {
    this._display = new OLEDDisplay(canvas);
    this._fb = new Framebuffer();
    this._state = State.SPLASH;
    this._app = null;
    this._splashT = 0;
    this._statusbar = new StatusBar();
    this._launcher = new Launcher();
    this._notif = new NotificationManager();
    this._sched = new Scheduler();
    this._input = new InputManager();
    this._onStateChange = null;
    this._registerApps(); this._registerTasks(); this._bindButtons();
  }
  set onStateChange(fn) { this._onStateChange = fn; }
  _registerApps() {
    const ex = () => this._goHome();
    const nx = (msg, dur) => this._notif.push(msg, dur);
    this._launcher.register('clock','Saat','clock',()=>this._open(new ClockApp(ex)));
    this._launcher.register('sysinfo','Sistem','cpu',()=>this._open(new SysInfoApp(ex)));
    this._launcher.register('wifi','WiFi','radar',()=>this._open(new WiFiApp(ex)));
    this._launcher.register('file','Dosya','script',()=>this._open(new FileBrowserApp(ex)));
    this._launcher.register('settings','Ayar','gear',()=>this._open(new SettingsApp(ex,nx)));
    this._launcher.register('power','Guc','service',()=>this._open(new PowerApp(ex)));
    this._launcher.register('snake','Yilan','snake',()=>this._open(new SnakeApp(ex)));
    this._launcher.register('flappy','Flappy','bird',()=>this._open(new FlappyApp(ex)));
    this._launcher.register('tamagotchi','Pet','pet',()=>this._open(new TamagotchiApp(ex)));
    this._launcher.register('dice','Zar','dice',()=>this._open(new DiceApp(ex)));
    this._launcher.register('graph','Grafik','graph',()=>this._open(new GraphApp(ex)));
    this._launcher.register('docker','Docker','docker',()=>this._open(new DockerApp(ex)));
    this._launcher.register('systemd','Svc','service',()=>this._open(new SystemdApp(ex)));
    this._launcher.register('gpio','GPIO','pin',()=>this._open(new GPIOViewerApp(ex)));
    this._launcher.register('i2c','I2C','i2c',()=>this._open(new I2CScannerApp(ex)));
    this._launcher.register('script','Komut','script',()=>this._open(new CommandRunnerApp(ex)));
    this._launcher.register('scope','Scope','scope',()=>this._open(new OscilloscopeApp(ex)));
    this._launcher.register('meter','Metre','volt',()=>this._open(new MultimeterApp(ex)));
    this._launcher.register('ssh','SSH','shield',()=>this._open(new SSHAlertApp(ex)));
    this._launcher.register('totp','TOTP','key',()=>this._open(new TOTPApp(ex)));
    this._launcher.register('passgen','Sifre','passkey',()=>this._open(new PasswordGeneratorApp(ex)));
    this._launcher.register('wifiscan','WiScan','radar',()=>this._open(new WiFiScannerApp(ex)));
    this._launcher.register('starfield','Yldiz','star',()=>this._open(new StarfieldApp(ex)));
    this._launcher.register('life','Life','cell',()=>this._open(new GameOfLifeApp(ex)));
    this._launcher.register('dvd','DVD','dvd',()=>this._open(new DVDLogoApp(ex)));
    this._launcher.register('matrix','Matrx','matrix',()=>this._open(new MatrixRainApp(ex)));
    this._launcher.register('crypto','Kripto','crypto',()=>this._open(new CryptoTickerApp(ex)));
    this._launcher.register('cube3d','3D','cube',()=>this._open(new Cube3DApp(ex)));
    this._launcher.register('fractal','Fraktl','fractal',()=>this._open(new FractalApp(ex)));
    this._launcher.register('qr','QR','qr',()=>this._open(new QRCodeApp(ex)));
    this._launcher.register('github','GitHub','github',()=>this._open(new GitHubTrackerApp(ex)));
    this._launcher.register('speed','Speed','speed',()=>this._open(new SpeedtestApp(ex)));
    this._launcher.register('news','HNews','news',()=>this._open(new HackerNewsApp(ex)));
    this._launcher.register('temp','Temp','temp',()=>this._open(new TemperatureHumidityApp(ex)));
    this._launcher.register('ups','UPS','ups',()=>this._open(new UPSBatteryApp(ex)));
    this._launcher.register('plant','Bitki','plant',()=>this._open(new PlantMonitorApp(ex)));
    this._launcher.register('compass','Pusula','compass',()=>this._open(new CompassApp(ex)));
    this._launcher.register('mp3','MP3','music',()=>this._open(new MP3PlayerApp(ex)));
    this._launcher.register('radio','Radyo','radio',()=>this._open(new RadioApp(ex)));
    this._launcher.register('video','Video','video',()=>this._open(new VideoPlayerApp(ex)));
    this._launcher.register('telegram','Tele','telegram',()=>this._open(new TelegramApp(ex)));
    this._launcher.register('email','Email','email',()=>this._open(new EmailApp(ex)));
    this._launcher.register('moon','Ay','moon',()=>this._open(new MoonApp(ex)));
    this._launcher.register('world','Dunya','world',()=>this._open(new WorldClockApp(ex)));
    this._launcher.register('pixel','Pixel','paint',()=>this._open(new PixelArtApp(ex)));
    this._launcher.register('shot','Shot','camera',()=>this._open(new ScreenshotApp(ex)));
    this._launcher.register('pomodoro','Pomo','timer',()=>this._open(new PomodoroApp(ex,nx)));
    this._launcher.register('breath','Nefes','breath',()=>this._open(new BreathingApp(ex)));
    this._launcher.register('hiit','HIIT','workout',()=>this._open(new HIITTimerApp(ex)));
    this._launcher.register('servo','Servo','servo',()=>this._open(new ServoControlApp(ex)));
    this._launcher.register('car','Araba','car',()=>this._open(new RobotCarApp(ex)));
    this._launcher.register('pihole','PiHole','pihole',()=>this._open(new PiHoleApp(ex)));
    this._launcher.register('ipcam','IPCam','camera',()=>this._open(new IPCameraApp(ex)));
    this._launcher.register('voice','Ses','mic',()=>this._open(new VoiceControlApp(ex)));
    this._launcher.register('sd','SD','sd',()=>this._open(new SDHealthApp(ex)));
    this._launcher.register('apt','APT','apt',()=>this._open(new APTUpdateApp(ex)));
    this._launcher.register('todo','Todo','todo',()=>this._open(new TodoApp(ex)));
    if (this._launcher.appCount !== 57) console.error(`Launcher parity error: expected 57 apps, got ${this._launcher.appCount}`);
  }
  _registerTasks(){this._sched.add('statusbar',()=>this._statusbar.update(),1.0);this._sched.add('notif',()=>this._notif.tick(),0.1);this._sched.add('app_update',()=>this._tickApp(),0.05);}
  _bindButtons(){this._input.on(EVT_UP,()=>this._onUp());this._input.on(EVT_DOWN,()=>this._onDown());this._input.on(EVT_SEL,()=>this._onSel());this._input.on(EVT_LONG,()=>this._onLong());}
  _open(app){this._app=app;this._state=State.APP;this._emitState();}
  _goHome(){this._app=null;this._state=State.HOME;this._emitState();}
  _emitState(){if(this._onStateChange){const names=['SPLASH','HOME','APP'];const app=this._app?(this._app.constructor.LABEL||this._app.constructor.NAME||'?'):'Launcher';this._onStateChange(names[this._state],app);}}
  _onUp(){if(this._state===State.HOME)this._launcher.moveUp();else if(this._state===State.APP&&this._app?.onUp)this._app.onUp();}
  _onDown(){if(this._state===State.HOME)this._launcher.moveDown();else if(this._state===State.APP&&this._app?.onDown)this._app.onDown();}
  _onSel(){if(this._state===State.HOME)this._launcher.select();else if(this._state===State.APP&&this._app?.onSel)this._app.onSel();}
  _onLong(){if(this._state===State.APP&&this._app?.onLong)this._app.onLong();else this._goHome();}
  _tickApp(){if(this._app?.update)this._app.update();}
  run(){this._input.start();this._notif.push('57 app simulator hazir!',2.0);this._emitState();const frameMs=1000/TARGET_FPS;let lastFrame=0;const loop=(ts)=>{if(ts-lastFrame>=frameMs){lastFrame=ts;this._sched.tick();this._render();}requestAnimationFrame(loop);};requestAnimationFrame(loop);}
  _render(){const fb=this._fb;fb.clear();if(this._state===State.SPLASH)this._drawSplash();else if(this._state===State.HOME){this._statusbar.draw(fb);this._launcher.draw(fb);}else if(this._state===State.APP&&this._app){this._statusbar.draw(fb);this._app.draw(fb);}if(this._notif.active)this._notif.draw(fb);this._display.render(fb);if(this._state===State.SPLASH){this._splashT++;if(this._splashT>=SPLASH_FRAMES){this._state=State.HOME;this._emitState();}}}
  _drawSplash(){const fb=this._fb,t=this._splashT;if(t<15)fb.circle(64,32,t*2,true,true);else{fb.circle(64,32,30,true,true);fb.textCentered('TinyOLED',20,false);fb.textCentered('57 App Web',30,false);fb.textCentered('Simulator',40,false);}if(t>=20){const progress=Math.min(1,(t-20)/(SPLASH_FRAMES-20)),barW=Math.floor(100*progress);fb.rect(14,56,100,5);if(barW>0)fb.rect(15,57,barW-1,3,true,true);}}
}
