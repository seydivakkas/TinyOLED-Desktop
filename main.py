"""
TinyOLED Desktop — Giriş Noktası
Raspberry Pi 3B+ + 0.96" SSD1306 OLED

Çalıştırma:
    sudo python3 main.py

Bağımlılıklar:
    sudo apt install python3-smbus2
    pip3 install RPi.GPIO
"""

import sys
import json
import logging
from pathlib import Path

# ── Loglama ────────────────────────────────────────────────────
logging.basicConfig(
    level   = logging.INFO,
    format  = "[%(levelname)s] %(name)s: %(message)s",
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/tmp/tinyoled.log"),
    ]
)
log = logging.getLogger("main")

# ── Yapılandırma ───────────────────────────────────────────────
CONFIG_PATH = Path(__file__).parent / "config" / "config.json"

def load_config() -> dict:
    try:
        return json.loads(CONFIG_PATH.read_text())
    except Exception as e:
        log.warning(f"config.json okunamadı ({e}), varsayılanlar kullanılıyor")
        return {}


def main():
    log.info("TinyOLED Desktop başlatılıyor...")
    config = load_config()

    # I2C ekran bağlantısı
    try:
        from core.display import SSD1306
        bus     = config.get("i2c_bus", 1)
        addr    = int(config.get("i2c_address", "0x3C"), 16)
        display = SSD1306(bus=bus, address=addr)
        log.info(f"SSD1306 bağlandı (bus={bus}, addr=0x{addr:02X})")
    except Exception as e:
        log.error(f"SSD1306 bağlantı hatası: {e}")
        log.error("I2C etkin mi? sudo raspi-config → Interface Options → I2C")
        sys.exit(1)

    # Parlaklık ayarla
    brightness = config.get("brightness", 200)
    display.brightness(brightness)

    # Masaüstü kabuğunu başlat
    from desktop.shell import Desktop
    desktop = Desktop(display)

    log.info("Masaüstü hazır — Ctrl+C ile çıkın")
    desktop.run()

    log.info("TinyOLED Desktop kapatıldı.")


if __name__ == "__main__":
    main()
