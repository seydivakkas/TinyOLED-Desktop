#!/bin/bash
# TinyOLED Desktop — Raspberry Pi OS Lite Kurulum Scripti
# Çalıştır: sudo bash install.sh

set -e

INSTALL_DIR="/home/pi/tiny-oled-desktop"
SERVICE_FILE="$INSTALL_DIR/service/tinyoled.service"

echo "========================================"
echo " TinyOLED Desktop Kurulumu"
echo " Raspberry Pi 3B+ + 0.96\" SSD1306 OLED"
echo "========================================"

# 1. I2C Etkinleştir
echo "[1/6] I2C arayüzü kontrol ediliyor..."
if ! grep -q "^dtparam=i2c_arm=on" /boot/config.txt; then
    echo "dtparam=i2c_arm=on" >> /boot/config.txt
    echo "   → I2C etkinleştirildi (yeniden başlatma gerekli)"
else
    echo "   → I2C zaten etkin"
fi

# 2. Sistem paketleri
echo "[2/6] Sistem paketleri kuruluyor..."
apt-get update -qq
apt-get install -y python3 python3-pip python3-smbus2 \
    i2c-tools wireless-tools wpasupplicant 2>/dev/null
echo "   → Sistem paketleri hazır"

# 3. Python kütüphaneleri
echo "[3/6] Python kütüphaneleri kuruluyor..."
pip3 install RPi.GPIO --quiet
echo "   → Python kütüphaneleri hazır"

# 4. Proje dosyalarını kopyala
echo "[4/6] Proje dosyaları kopyalanıyor..."
mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR/"
chown -R pi:pi "$INSTALL_DIR"
echo "   → Dosyalar: $INSTALL_DIR"

# 5. Systemd servisi
echo "[5/6] Systemd servisi kuruluyor..."
cp "$SERVICE_FILE" /etc/systemd/system/tinyoled.service
systemctl daemon-reload
systemctl enable tinyoled.service
echo "   → Servis aktif edildi"

# 6. I2C cihaz testi
echo "[6/6] I2C taraması yapılıyor..."
i2cdetect -y 1 2>/dev/null || echo "   → i2cdetect başarısız (I2C aktif değil olabilir)"

echo ""
echo "========================================"
echo " Kurulum Tamamlandı!"
echo "========================================"
echo ""
echo " Bağlantı şeması:"
echo "   OLED SDA  → GPIO 2  (Pin 3)"
echo "   OLED SCL  → GPIO 3  (Pin 5)"
echo "   OLED VCC  → 3.3V    (Pin 1)"
echo "   OLED GND  → GND     (Pin 6)"
echo ""
echo "   BTN UP    → GPIO 17 (Pin 11) + GND"
echo "   BTN DOWN  → GPIO 27 (Pin 13) + GND"
echo "   BTN SEL   → GPIO 22 (Pin 15) + GND"
echo ""
echo " Manuel çalıştırma:"
echo "   sudo python3 $INSTALL_DIR/main.py"
echo ""
echo " Servis komutları:"
echo "   sudo systemctl start  tinyoled"
echo "   sudo systemctl stop   tinyoled"
echo "   sudo systemctl status tinyoled"
echo "   journalctl -u tinyoled -f"
echo ""
echo " NOT: I2C için sistem yeniden başlatılmalı!"
echo "   sudo reboot"
