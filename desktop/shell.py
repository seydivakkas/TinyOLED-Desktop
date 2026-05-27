"""
TinyOLED Desktop — Ana Masaüstü Kabuğu
Tüm bileşenleri bir araya getirir:
  StatusBar + Launcher + App yönetimi + Bildirimler + Zamanlayıcı

Durum makinesi:
  HOME   → Launcher göster
  APP    → Aktif uygulama göster
  SPLASH → Açılış animasyonu
"""

import time
from enum import Enum, auto
from typing import Optional, Any

from core.framebuffer import Framebuffer
from core.display     import SSD1306
from core.input       import ButtonManager, EVT_UP, EVT_DOWN, EVT_SEL, EVT_LONG
from core.scheduler   import Scheduler
from core.font        import Font

from desktop.statusbar    import StatusBar
from desktop.launcher     import Launcher
from desktop.notification import NotificationManager

from apps.clock       import ClockApp
from apps.sysinfo     import SysInfoApp
from apps.wifi        import WiFiApp
from apps.filebrowser import FileBrowserApp
from apps.settings    import SettingsApp
from apps.power       import PowerApp

# ── Yeni Uygulamalar ──────────────────────────────────────────
from apps.snake          import SnakeApp
from apps.flappy         import FlappyApp
from apps.tamagotchi     import TamagotchiApp
from apps.dice           import DiceApp
from apps.graph          import GraphApp
from apps.docker_mon     import DockerMonApp
from apps.systemd_mon    import SystemdMonApp
from apps.gpio_viewer    import GPIOViewerApp
from apps.i2c_scan       import I2CScanApp
from apps.script_runner  import ScriptRunnerApp
from apps.oscilloscope   import OscilloscopeApp
from apps.multimeter     import MultimeterApp
from apps.ssh_alert      import SSHAlertApp
from apps.totp           import TOTPApp
from apps.passgen        import PassGenApp
from apps.wifi_scan      import WiFiScanApp
from apps.ss_starfield   import StarfieldApp
from apps.ss_gameoflife  import GameOfLifeApp
from apps.ss_dvd         import DVDLogoApp
from apps.ss_matrix      import MatrixRainApp
from apps.crypto         import CryptoApp
from apps.cube3d         import Cube3DApp
from apps.fractal        import FractalApp
from apps.qrcode_gen     import QRCodeGenApp
from apps.github_tracker import GitHubTrackerApp
from apps.speedtest_app  import SpeedtestApp
from apps.hackernews     import HackerNewsApp
from apps.sensors        import SensorsApp
from apps.ups_battery    import UPSBatteryApp
from apps.plant_monitor  import PlantMonitorApp
from apps.compass        import CompassApp
from apps.mp3player      import MP3PlayerApp
from apps.radio          import RadioApp
from apps.videoplayer    import VideoPlayerApp
from apps.telegram_bot   import TelegramBotApp
from apps.email_counter  import EmailCounterApp
from apps.moon           import MoonApp
from apps.worldclock     import WorldClockApp
from apps.pixelart       import PixelArtApp
from apps.screenshot     import ScreenshotApp
from apps.pomodoro       import PomodoroApp
from apps.breathing      import BreathingApp
from apps.workout        import WorkoutApp
from apps.servo          import ServoApp
from apps.rc_car         import RCCarApp
from apps.pihole         import PiholeApp
from apps.ipcam          import IPCamApp
from apps.voice          import VoiceApp
from apps.sd_health      import SDHealthApp
from apps.apt_update     import APTUpdateApp
from apps.todo           import TodoApp


class State(Enum):
    SPLASH = auto()
    HOME   = auto()
    APP    = auto()


SPLASH_FRAMES = 40    # ~2 saniye @ 20fps
TARGET_FPS    = 20
FRAME_MS      = 1.0 / TARGET_FPS


class Desktop:
    """
    TinyOLED Desktop ana döngüsü.
    main.py tarafından başlatılır.
    """

    def __init__(self, display: SSD1306):
        self._display  = display
        self._fb       = Framebuffer()
        self._state    = State.SPLASH
        self._app      = None          # Aktif uygulama nesnesi
        self._splash_t = 0

        # Alt sistem bileşenleri
        self._statusbar = StatusBar()
        self._launcher  = Launcher()
        self._notif     = NotificationManager()
        self._sched     = Scheduler()
        self._input     = ButtonManager()

        self._register_apps()
        self._register_tasks()
        self._bind_buttons()

    # ── Uygulama Kaydı ────────────────────────────────────────
    def _register_apps(self):
        d  = self._display
        nx = self._notif.push
        ex = self._go_home

        # ── Orijinal Uygulamalar ──
        self._launcher.register("clock",    "Saat",   "clock",    lambda: self._open(ClockApp(ex)))
        self._launcher.register("sysinfo",  "Sistem", "cpu",      lambda: self._open(SysInfoApp(ex)))
        self._launcher.register("wifi",     "WiFi",   "wifi",     lambda: self._open(WiFiApp(ex, nx)))
        self._launcher.register("files",    "Dosya",  "folder",   lambda: self._open(FileBrowserApp(ex, nx)))
        self._launcher.register("settings", "Ayar",   "gear",     lambda: self._open(SettingsApp(ex, nx, d)))
        self._launcher.register("power",    "Guc",    "power",    lambda: self._open(PowerApp(ex, nx, d)))

        # ── Oyunlar ──
        self._launcher.register("snake",    "Yilan",  "snake",    lambda: self._open(SnakeApp(ex)))
        self._launcher.register("flappy",   "Flappy", "bird",     lambda: self._open(FlappyApp(ex)))
        self._launcher.register("tamagotchi","Pet",   "pet",      lambda: self._open(TamagotchiApp(ex)))
        self._launcher.register("dice",     "Zar",    "dice",     lambda: self._open(DiceApp(ex)))

        # ── İzleme & Grafik ──
        self._launcher.register("graph",    "Graf",   "graph",    lambda: self._open(GraphApp(ex)))
        self._launcher.register("docker",   "Dockr",  "docker",   lambda: self._open(DockerMonApp(ex, nx)))
        self._launcher.register("systemd",  "Servi",  "service",  lambda: self._open(SystemdMonApp(ex, nx)))

        # ── Geliştirici Araçları ──
        self._launcher.register("gpio",     "GPIO",   "pin",      lambda: self._open(GPIOViewerApp(ex)))
        self._launcher.register("i2c",      "I2C",    "i2c",      lambda: self._open(I2CScanApp(ex)))
        self._launcher.register("scripts",  "Komut",  "script",   lambda: self._open(ScriptRunnerApp(ex, nx)))
        self._launcher.register("scope",    "Scope",  "scope",    lambda: self._open(OscilloscopeApp(ex)))
        self._launcher.register("volt",     "Volt",   "volt",     lambda: self._open(MultimeterApp(ex)))

        # ── Güvenlik ──
        self._launcher.register("sshalert", "SSH",    "shield",   lambda: self._open(SSHAlertApp(ex, nx)))
        self._launcher.register("totp",     "2FA",    "key",      lambda: self._open(TOTPApp(ex)))
        self._launcher.register("passgen",  "Sifre",  "passkey",  lambda: self._open(PassGenApp(ex)))
        self._launcher.register("wifiscan", "Tara",   "radar",    lambda: self._open(WiFiScanApp(ex)))

        # ── Ekran Koruyucular ──
        self._launcher.register("starfield","Yldiz",  "star",     lambda: self._open(StarfieldApp(ex)))
        self._launcher.register("life",     "Life",   "cell",     lambda: self._open(GameOfLifeApp(ex)))
        self._launcher.register("dvd",      "DVD",    "dvd",      lambda: self._open(DVDLogoApp(ex)))
        self._launcher.register("matrix",   "Matrx",  "matrix",   lambda: self._open(MatrixRainApp(ex)))

        # ── Finans & 3D ──
        self._launcher.register("crypto",   "Kripto", "crypto",   lambda: self._open(CryptoApp(ex)))
        self._launcher.register("cube3d",   "3D",     "cube",     lambda: self._open(Cube3DApp(ex)))
        self._launcher.register("fractal",  "Fraktl", "fractal",  lambda: self._open(FractalApp(ex)))

        # ── Akıllı Araçlar ──
        self._launcher.register("qrcode",   "QR",     "qr",       lambda: self._open(QRCodeGenApp(ex)))
        self._launcher.register("github",   "Git",    "github",   lambda: self._open(GitHubTrackerApp(ex)))
        self._launcher.register("speedtest","Hiz",    "speed",    lambda: self._open(SpeedtestApp(ex)))
        self._launcher.register("hackernews","HN",    "news",     lambda: self._open(HackerNewsApp(ex)))

        # ── Sensörler ──
        self._launcher.register("sensors",  "Sensr",  "temp",     lambda: self._open(SensorsApp(ex)))
        self._launcher.register("ups",      "UPS",    "ups",      lambda: self._open(UPSBatteryApp(ex)))
        self._launcher.register("plant",    "Bitki",  "plant",    lambda: self._open(PlantMonitorApp(ex)))
        self._launcher.register("compass",  "Pusla",  "compass",  lambda: self._open(CompassApp(ex)))

        # ── Medya ──
        self._launcher.register("mp3",      "Muzik",  "music",    lambda: self._open(MP3PlayerApp(ex)))
        self._launcher.register("radio",    "Radyo",  "radio",    lambda: self._open(RadioApp(ex)))
        self._launcher.register("video",    "Video",  "video",    lambda: self._open(VideoPlayerApp(ex)))

        # ── Mesajlaşma ──
        self._launcher.register("telegram", "Telgm",  "telegram", lambda: self._open(TelegramBotApp(ex)))
        self._launcher.register("email",    "Email",  "email",    lambda: self._open(EmailCounterApp(ex)))

        # ── Astronomi ──
        self._launcher.register("moon",     "Ay",     "moon",     lambda: self._open(MoonApp(ex)))
        self._launcher.register("worldclock","Dunya",  "world",   lambda: self._open(WorldClockApp(ex)))

        # ── Yaratıcı ──
        self._launcher.register("pixelart", "Pixel",  "paint",    lambda: self._open(PixelArtApp(ex)))
        self._launcher.register("screenshot","SS",    "camera",   lambda: self._open(ScreenshotApp(ex, nx)))

        # ── Sağlık & Fitness ──
        self._launcher.register("pomodoro", "Pomo",   "timer",    lambda: self._open(PomodoroApp(ex, nx)))
        self._launcher.register("breath",   "Nefes",  "breath",   lambda: self._open(BreathingApp(ex)))
        self._launcher.register("workout",  "HIIT",   "workout",  lambda: self._open(WorkoutApp(ex, nx)))

        # ── Robotik ──
        self._launcher.register("servo",    "Servo",  "servo",    lambda: self._open(ServoApp(ex)))
        self._launcher.register("rc_car",   "Araba",  "car",      lambda: self._open(RCCarApp(ex)))

        # ── Ağ ──
        self._launcher.register("pihole",   "Pi-h",   "pihole",   lambda: self._open(PiholeApp(ex)))
        self._launcher.register("ipcam",    "Kamera", "camera",   lambda: self._open(IPCamApp(ex)))

        # ── Ses ──
        self._launcher.register("voice",    "Ses",    "mic",      lambda: self._open(VoiceApp(ex, nx)))

        # ── Bakım ──
        self._launcher.register("sdhealth", "SD",     "sd",       lambda: self._open(SDHealthApp(ex)))
        self._launcher.register("apt",      "APT",    "apt",      lambda: self._open(APTUpdateApp(ex, nx)))
        self._launcher.register("todo",     "Gorev",  "todo",     lambda: self._open(TodoApp(ex)))

    def _register_tasks(self):
        self._sched.add("statusbar", self._statusbar.update, interval=1.0)
        self._sched.add("notif",     self._notif.tick,        interval=0.1)
        self._sched.add("app_update",self._tick_app,          interval=1.0)

    def _bind_buttons(self):
        b = self._input
        b.on(EVT_UP,   self._on_up)
        b.on(EVT_DOWN, self._on_down)
        b.on(EVT_SEL,  self._on_sel)
        b.on(EVT_LONG, self._on_long)

    # ── Durum Geçişleri ────────────────────────────────────────
    def _open(self, app):
        self._app   = app
        self._state = State.APP

    def _go_home(self):
        self._app   = None
        self._state = State.HOME

    # ── Buton Olayları ─────────────────────────────────────────
    def _on_up(self):
        if self._state == State.HOME:
            self._launcher.move_up()
        elif self._state == State.APP and hasattr(self._app, "on_up"):
            self._app.on_up()

    def _on_down(self):
        if self._state == State.HOME:
            self._launcher.move_down()
        elif self._state == State.APP and hasattr(self._app, "on_down"):
            self._app.on_down()

    def _on_sel(self):
        if self._state == State.HOME:
            self._launcher.select()
        elif self._state == State.APP and hasattr(self._app, "on_sel"):
            self._app.on_sel()

    def _on_long(self):
        if self._state == State.APP and hasattr(self._app, "on_long"):
            self._app.on_long()
        else:
            self._go_home()

    def _tick_app(self):
        if self._app and hasattr(self._app, "update"):
            self._app.update()

    # ── Ana Döngü ──────────────────────────────────────────────
    def run(self):
        """Bloklayan ana döngü. Ctrl+C ile durdurulur."""
        self._input.start()
        self._notif.push("TinyOLED v1.0 hazir!", duration=2.0)

        try:
            while True:
                frame_start = time.monotonic()

                self._sched.tick()
                self._render()

                elapsed = time.monotonic() - frame_start
                sleep_t = max(0.0, FRAME_MS - elapsed)
                if sleep_t > 0:
                    time.sleep(sleep_t)

        except KeyboardInterrupt:
            pass
        finally:
            self._fb.clear()
            self._fb.flush(self._display)
            self._display.power(False)
            self._input.stop()

    # ── Render ─────────────────────────────────────────────────
    def _render(self):
        fb = self._fb
        fb.clear()

        if self._state == State.SPLASH:
            self._draw_splash()
        elif self._state == State.HOME:
            self._statusbar.draw(fb)
            self._launcher.draw(fb)
        elif self._state == State.APP and self._app:
            self._statusbar.draw(fb)
            self._app.draw(fb)

        if self._notif.active:
            self._notif.draw(fb)

        fb.flush(self._display)

        # Splash'ten HOME'a geçiş
        if self._state == State.SPLASH:
            self._splash_t += 1
            if self._splash_t >= SPLASH_FRAMES:
                self._state = State.HOME

    def _draw_splash(self):
        fb = self._fb
        t  = self._splash_t

        # Logo animasyonu: dairesel açılma
        if t < 15:
            r = t * 2
            fb.circle(64, 32, r, fill=True)
        else:
            fb.circle(64, 32, 30, fill=True)
            # Logo metni (siyah üzerine beyaz)
            fb.text_centered("TinyOLED", 22, on=False)
            fb.text_centered("Desktop v1.0", 31, on=False)
            fb.text_centered("Pi 3B+", 40, on=False)

        # Alt yükleme çubuğu
        if t >= 20:
            progress = min(1.0, (t - 20) / (SPLASH_FRAMES - 20))
            bar_w    = int(100 * progress)
            fb.rect(14, 56, 100, 5)
            if bar_w > 0:
                fb.rect(15, 57, bar_w - 1, 3, fill=True)
