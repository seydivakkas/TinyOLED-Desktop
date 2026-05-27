"""
TinyOLED Desktop — GPIO Button Input Manager
Raspberry Pi 3B+ GPIO pinout:

    [UP]    → GPIO 17  (Pin 11) — Yukarı / Geri
    [DOWN]  → GPIO 27  (Pin 13) — Aşağı / İleri
    [SEL]   → GPIO 22  (Pin 15) — Seç / Enter / Onayla

Butonlar iç pull-up dirençleri ile kullanılır.
Basıldığında LOW (0V), bırakıldığında HIGH (3.3V).
"""

import threading
import time
from typing import Callable, Dict, Optional

try:
    import RPi.GPIO as GPIO
    _HW = True
except ImportError:
    # Geliştirme ortamı (PC) için sahte GPIO
    _HW = False
    class _FakeGPIO:
        BCM = IN = FALLING = PUD_UP = None
        @staticmethod
        def setmode(_): pass
        @staticmethod
        def setup(_, __, pull_up_down=None): pass
        @staticmethod
        def add_event_detect(_, __, callback=None, bouncetime=None): pass
        @staticmethod
        def cleanup(): pass
        @staticmethod
        def input(_): return 1
    GPIO = _FakeGPIO()
    print("[INPUT] RPi.GPIO bulunamadı — simülasyon modunda çalışıyor.")


# ── Pin Tanımları ──────────────────────────────────────────────
PIN_UP   = 17
PIN_DOWN = 27
PIN_SEL  = 22

BOUNCE_MS = 200   # debounce süresi (ms)

# ── Olay Sabitleri ─────────────────────────────────────────────
EVT_UP   = "UP"
EVT_DOWN = "DOWN"
EVT_SEL  = "SEL"
EVT_LONG = "LONG"   # uzun basma (>800ms)

LONG_PRESS_MS = 800


class ButtonManager:
    """
    3 GPIO butonu dinler ve olay callback'lerini ateşler.

    Kullanım:
        bm = ButtonManager()
        bm.on(EVT_UP,  lambda: print("Yukarı"))
        bm.on(EVT_SEL, lambda: print("Seç"))
        bm.start()
        ...
        bm.stop()
    """

    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        self._press_time: Dict[int, float] = {}
        self._running = False
        self._lock = threading.Lock()

        GPIO.setmode(GPIO.BCM)
        for pin in (PIN_UP, PIN_DOWN, PIN_SEL):
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # ── Callback kaydı ────────────────────────────────────────
    def on(self, event: str, callback: Callable):
        """Olay için callback kaydet."""
        self._handlers[event] = callback

    def emit(self, event: str):
        """Bir olayı elle tetikle (simülasyon / test için)."""
        handler = self._handlers.get(event)
        if handler:
            try:
                handler()
            except Exception as e:
                print(f"[INPUT] Handler hatası ({event}): {e}")

    # ── GPIO Başlat ────────────────────────────────────────────
    def start(self):
        """GPIO interrupt'larını etkinleştir."""
        if not _HW:
            return
        self._running = True
        GPIO.add_event_detect(
            PIN_UP,   GPIO.FALLING,
            callback=lambda _: self._on_press(PIN_UP,   EVT_UP),
            bouncetime=BOUNCE_MS,
        )
        GPIO.add_event_detect(
            PIN_DOWN, GPIO.FALLING,
            callback=lambda _: self._on_press(PIN_DOWN, EVT_DOWN),
            bouncetime=BOUNCE_MS,
        )
        GPIO.add_event_detect(
            PIN_SEL,  GPIO.FALLING,
            callback=lambda _: self._on_press(PIN_SEL,  EVT_SEL),
            bouncetime=BOUNCE_MS,
        )

    def stop(self):
        """GPIO'yu serbest bırak."""
        self._running = False
        GPIO.cleanup()

    # ── Dahili ────────────────────────────────────────────────
    def _on_press(self, pin: int, event: str):
        now = time.monotonic()
        self._press_time[pin] = now

        # Uzun basma tespiti için arka plan thread
        threading.Thread(
            target=self._check_long,
            args=(pin, now),
            daemon=True,
        ).start()

        self.emit(event)

    def _check_long(self, pin: int, start: float):
        time.sleep(LONG_PRESS_MS / 1000)
        with self._lock:
            # Hâlâ basılıysa → uzun basma
            if _HW and GPIO.input(pin) == 0:
                self.emit(EVT_LONG)
