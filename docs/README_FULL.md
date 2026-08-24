<p align="center">
  <img src="docs/banner.png" alt="TinyOLED Desktop" width="600">
</p>

<h1 align="center">🖥️ TinyOLED Desktop</h1>

<p align="center">
  <strong>Raspberry Pi + 0.96" SSD1306 OLED için Tam Donanımlı Masaüstü İşletim Sistemi</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Raspberry%20Pi-red?style=flat-square&logo=raspberrypi" alt="Platform">
  <img src="https://img.shields.io/badge/display-SSD1306%20128×64-blue?style=flat-square" alt="Display">
  <img src="https://img.shields.io/badge/language-Python%203-yellow?style=flat-square&logo=python" alt="Language">
  <img src="https://img.shields.io/badge/apps-57+-green?style=flat-square" alt="Apps">
  <img src="https://img.shields.io/badge/simulator-Live%20Demo-ff6600?style=flat-square&logo=googlechrome" alt="Live Demo">
  <img src="https://img.shields.io/badge/license-All%20Rights%20Reserved-red?style=flat-square" alt="License">
</p>

<p align="center">
  <em>128×64 piksel monokrom ekran üzerinde çalışan, 3 fiziksel düğme ile kontrol edilen,<br>
  57 uygulamalı tam bir masaüstü deneyimi.</em>
</p>

<p align="center">
  <a href="https://seydivakkas.github.io/TinyOLED-Desktop/">
    <img src="https://img.shields.io/badge/🖥️_Canlı_Demo_—_Tarayıcıda_Dene!-00e5ff?style=for-the-badge&logoColor=white" alt="Live Demo">
  </a>
</p>

---

```
┌──────────────────────────────────────┐
│  12:34  |  🌐 WiFi  |  🔋 85%       │  ← Status Bar (10px)
├──────┬──────┬──────┬──────┬──────┬───┤
│  🕐  │  💻  │  📡  │  📁  │  ⚙️  │ ⏻ │
│ Saat │Sistem│ WiFi │Dosya │ Ayar │Güç│  ← Launcher Grid (3×2)
├──────┴──────┴──────┴──────┴──────┴───┤
│  🎮  │  🐦  │  🐾  │  🎲  │  📈  │🐳│
│Yılan │Flappy│ Pet  │ Zar  │ Graf │Doc│  ← Sayfa 2
├──────┴──────┴──────┴──────┴──────┴───┤
│          ● ● ○ ○ ○ ○ ○ ○ ○ ○        │  ← 10 Sayfa Göstergesi
└──────────────────────────────────────┘
```

## 📖 Proje Hakkında

**TinyOLED Desktop**, Raspberry Pi ailesine (Zero W, 3B+, 4, 5) bağlı 0.96 inçlik SSD1306 OLED ekranı tam bir masaüstü işletim sistemine dönüştüren açık kaynaklı bir projedir.

Tüm sistem sıfırdan, herhangi bir GUI framework'ü kullanmadan yazılmıştır. Piksel piksel çizim yapan özel bir **framebuffer motoru**, **5×7 bitmap font renderer**, **8×8 monokrom ikon seti** ve **kooperatif görev zamanlayıcısı** içerir.

### Neden Bu Proje?

- 🧠 **Eğitim:** Gömülü sistemler, I2C protokolü, framebuffer mimarisi ve durum makinesi tasarımını pratikte öğretir
- ⚡ **Hafif:** Toplam bellek ayak izi ~2KB (128×64÷8 = 1024 byte framebuffer). GUI framework gerektirmez
- 🔌 **Genişletilebilir:** Her yeni uygulama tek bir Python dosyasıdır. Standardize edilmiş arayüz sözleşmesiyle dakikalar içinde yeni uygulama yazılabilir
- 🎮 **Eğlenceli:** Yılan oyunundan kripto takipçisine, TOTP authenticator'dan nefes egzersizine kadar 57 farklı uygulama
- 🌐 **Web Simülatör:** Raspberry Pi olmadan tarayıcıda hemen deneyin! Tüm sistemi piksel-mükemmel olarak simüle eder

---

## 🌐 Web Simülatör — Tarayıcıda Canlı Demo

> **Raspberry Pi'niz yok mu? Sorun değil!** Tüm TinyOLED Desktop deneyimini tarayıcınızda yaşayın.

<p align="center">
  <a href="https://seydivakkas.github.io/TinyOLED-Desktop/">
    <strong>👉 seydivakkas.github.io/TinyOLED-Desktop 👈</strong>
  </a>
</p>

Web simülatör, gerçek donanımı olmadan TinyOLED Desktop'ı tam olarak deneyimlemenizi sağlar. Python kaynak kodu satır satır JavaScript'e port edilmiştir — aynı framebuffer motoru, aynı font verisi, aynı çizim primitifleri.

### ✨ Simülatör Özellikleri

| Özellik | Detay |
|---------|-------|
| 🎨 **Piksel-Mükemmel Render** | 128×64 piksel, gerçek SSD1306 page formatı, OLED glow efekti |
| ⌨️ **Klavye Kontrolleri** | `W`/`↑` Yukarı, `S`/`↓` Aşağı, `Enter`/`Space` Seç, `Esc` Geri |
| 📱 **Dokunmatik Düğmeler** | Mobil uyumlu ekran üstü ▲ ▼ ● düğmeleri |
| 🖥️ **PCB Kartı Tasarımı** | Gerçekçi baskılı devre görünümü, lehim delikleri, bakır yollar |
| 🎮 **15 Çalışan Uygulama** | Saat, Yılan, Flappy Bird, 3D Küp, Fraktal, Matrix Rain ve daha fazlası |
| 🔄 **20 FPS Animasyon** | requestAnimationFrame tabanlı akıcı render döngüsü |

### 🎮 Simülatördeki Uygulamalar

```
┌──────────────────────────────────────────────────────────────┐
│  🕐 Saat (Analog+Dijital)  │  💻 Sistem Bilgisi (4 sayfa)  │
│  🐍 Yılan Oyunu            │  🐦 Flappy Bird               │
│  🎲 Zar Simülatörü (D4-D20)│  🧊 3D Tel Kafes Küp          │
│  🌀 Mandelbrot Fraktal     │  🧘 Nefes Egzersizi (4-7-8)   │
│  🌙 Ay Evresi (gerçek)     │  🍅 Pomodoro Zamanlayıcı      │
│  ⭐ Starfield 3D           │  💚 Matrix Digital Rain        │
│  🧬 Conway's Game of Life  │  📀 DVD Bouncing Logo          │
│  ⚙️ Ayarlar                │                                │
└──────────────────────────────────────────────────────────────┘
```

### 🚀 Lokalde Çalıştırma

```bash
# Web simülatörü lokalde başlat
cd web-simulator
px serve
# → http://localhost:3000 adresinde açılır
```

---

## 🛠️ Donanım Gereksinimleri

### Minimum (Zorunlu)

| Bileşen | Model | Bağlantı | Not |
|---------|-------|----------|-----|
| **SBC** | Raspberry Pi (herhangi bir model) | — | Zero W, 3B+, 4, 5 desteklenir |
| **Ekran** | SSD1306 OLED 0.96" (128×64) | I2C | 4 pin: VCC, GND, SDA, SCL |
| **Düğme ×3** | Tactile push button | GPIO + GND | Pull-up dirençli (dahili) |

### İsteğe Bağlı (Ek Uygulamalar İçin)

| Bileşen | Destekleyen Uygulama | Bağlantı |
|---------|---------------------|----------|
| DHT11 / DHT22 | 🌡️ Sensör İstasyonu | GPIO 4 |
| MCP3008 ADC | 📡 Osiloskop, 🪴 Bitki Monitörü | SPI |
| INA219 | ⚡ Multimetre, 🔋 UPS Pil | I2C (0x40) |
| HMC5883L | 🧭 Pusula | I2C (0x1E) |
| Servo Motor (SG90) | 🦾 Servo Kontrol | GPIO 18 (PWM) |
| L298N Motor Sürücü | 🚗 Robot Araba | GPIO 23,24,5,6 |
| Toprak Nem Sensörü | 🪴 Bitki Sulama | ADC üzerinden |
| UPS HAT / PiJuice | 🔋 UPS Pil Durumu | I2C (0x36) |
| Hoparlör / DAC | 🎵 MP3 Çalar, 📻 Radyo | 3.5mm veya I2S |
| USB Mikrofon | 🎙️ Sesli Kontrol | USB |

### Bağlantı Şeması

```
Raspberry Pi GPIO Header
─────────────────────────────────────

                3.3V [1]  [2]  5V
 OLED SDA ─── GPIO2 [3]  [4]  5V
 OLED SCL ─── GPIO3 [5]  [6]  GND ─── OLED GND
              GPIO4 [7]  [8]  GPIO14
                GND [9]  [10] GPIO15
 BTN UP ──── GPIO17 [11] [12] GPIO18 ─── Servo PWM
 BTN DOWN ── GPIO27 [13] [14] GND
 BTN SEL ─── GPIO22 [15] [16] GPIO23
              3.3V  [17] [18] GPIO24
                    ...
```

> **Not:** Düğmeler GPIO pini ile GND arasına bağlanır. Dahili pull-up dirençleri yazılımda aktif edilir.

---

## 🚀 Hızlı Kurulum

### Tek Komutla Kurulum

```bash
git clone https://github.com/seydivakkas/TinyOLED-Desktop.git
cd TinyOLED-Desktop
sudo bash install.sh
sudo reboot
```

### Manuel Kurulum

```bash
# 1. I2C'yi etkinleştir
sudo raspi-config
# → Interface Options → I2C → Enable

# 2. Sistem paketleri
sudo apt update
sudo apt install -y python3 python3-pip python3-smbus2 i2c-tools

# 3. Python bağımlılıkları
pip3 install RPi.GPIO

# 4. İsteğe bağlı (ek uygulamalar için)
pip3 install qrcode         # QR Kod üreteci
sudo apt install mpv        # MP3 Çalar & Radyo

# 5. I2C bağlantısını doğrula
sudo i2cdetect -y 1
# 0x3C adresinde SSD1306 görünmelidir

# 6. Çalıştır
sudo python3 main.py
```

### Sistem Servisi Olarak Çalıştırma

Raspberry Pi her açıldığında TinyOLED Desktop'ın otomatik başlaması için:

```bash
sudo cp service/tinyoled.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tinyoled
sudo systemctl start tinyoled

# Durum kontrolü
sudo systemctl status tinyoled
journalctl -u tinyoled -f
```

---

## 📱 Uygulama Kataloğu (57 Uygulama)

### 🏠 Sistem Uygulamaları (6)

| Uygulama | Açıklama | Kontroller |
|----------|----------|-----------|
| 🕐 **Saat** | Analog ve dijital saat görünümü | UP/DOWN: Görünüm değiştir |
| 💻 **Sistem** | CPU, RAM, sıcaklık, IP, uptime bilgileri | UP/DOWN: Metrik gezin |
| 📡 **WiFi** | Ağ tarama, bağlanma, bağlantı kesme | UP/DOWN: Ağ seç, SEL: Bağlan |
| 📁 **Dosya** | Dosya sistemi tarayıcı | UP/DOWN: Gezin, SEL: Aç/Gir |
| ⚙️ **Ayarlar** | Parlaklık, kontrast, FPS ayarları | UP/DOWN: Seç, SEL: Değiştir |
| ⏻ **Güç** | Uyku modu, yeniden başlatma, kapatma | UP/DOWN: Seç, SEL: Uygula |

---

### 🎮 Oyunlar (4)

| Uygulama | Açıklama | Kontroller |
|----------|----------|-----------|
| 🐍 **Yılan** | Klasik yılan oyunu. Rotasyon tabanlı kontrol, wrap-around hareket, skor sistemi | UP: Saat yönü, DOWN: Ters yön, SEL: Yeniden başlat |
| 🐦 **Flappy Bird** | Flappy Bird klonu. Yerçekimi fiziği, boru engelleri, çarpışma tespiti | UP/SEL: Zıpla, SEL: Yeniden başlat |
| 🐾 **Tamagotchi** | Sanal evcil hayvan. Açlık, mutluluk, enerji, temizlik barları. Durum JSON'da saklanır | UP/DOWN: Aksiyon seç, SEL: Uygula |
| 🎲 **Zar** | D4, D6, D8, D10, D12, D20 destekli animasyonlu zar simülatörü | UP/DOWN: Zar tipi, SEL: At |

---

### 📈 İzleme & Grafik (3)

| Uygulama | Açıklama |
|----------|----------|
| 📊 **Gerçek Zamanlı Grafik** | CPU kullanımı, RAM yüzdesi veya sıcaklığı canlı çizgi grafiği olarak gösterir. 100 noktalık `deque` geçmişi |
| 🐳 **Docker Monitör** | Çalışan Docker konteynerlerini listeler. Başlat/durdur toggle. `docker ps` çıktısını işler |
| 🔄 **Systemd Yöneticisi** | Kritik servislerin (ssh, nginx, docker, cron) durumunu izler. `SEL` ile servis yeniden başlatılır |

---

### 🛠️ Geliştirici Araçları (5)

| Uygulama | Açıklama |
|----------|----------|
| 📌 **GPIO Viewer** | 28 GPIO pininin gerçek zamanlı HIGH/LOW durumunu gösterir. Çıkış pinleri toggle edilebilir |
| 🔍 **I2C Scanner** | I2C bus üzerinde 0x00-0x77 adres taraması yaparak bağlı cihazları görsel bir grid'de gösterir |
| 📜 **Komut Çalıştırıcı** | `config/commands.json` dosyasından hazır bash komutlarını seçip arka planda çalıştırır |
| 📡 **Osiloskop** | MCP3008 ADC üzerinden analog sinyalleri örnekleyerek dalga formunu gerçek zamanlı çizer. Donanım yokken sinüs dalga simülasyonu yapar |
| ⚡ **Multimetre** | INA219 sensörü üzerinden voltaj (V), akım (mA) ve güç (W) değerlerini büyük rakamlarla gösterir |

---

### 🔐 Güvenlik (4)

| Uygulama | Açıklama |
|----------|----------|
| 🛡️ **SSH Alert** | `/var/log/auth.log` dosyasını arka planda izler. Başarısız giriş denemelerini IP adresiyle bildirir |
| 🔑 **TOTP 2FA** | RFC 6238 uyumlu TOTP (Time-based One-Time Password) üreteci. Google Authenticator benzeri 6 haneli kodlar üretir. 30 saniye döngü ile progress bar |
| 🔒 **Şifre Üreteci** | `SystemRandom` ile kriptografik kalitede rastgele şifreler üretir. Uzunluk: 8-24 karakter ayarlanabilir |
| 📡 **WiFi Tarayıcı** | Çevredeki WiFi ağlarını SSID, kanal, sinyal gücü ve şifreleme tipiyle listeler |

---

### 🌌 Ekran Koruyucular (4)

| Uygulama | Açıklama |
|----------|----------|
| ⭐ **Starfield** | 3D perspektif projeksiyonlu yıldız geçidi. Yıldızlar yaklaştıkça büyür |
| 🧬 **Game of Life** | Conway'in Hayat Oyunu. 128×64 piksel = 8.192 hücre. Tam çözünürlükte hücresel otomat |
| 📀 **DVD Logo** | Zıplayan "TinyOLED" logosu. Duvara çarptığında renk (invert) değiştirir |
| 💚 **Matrix Rain** | Matrix filmi tarzı dikey akan rastgele karakter yağmuru. 21 sütun, 8 satır |

---

### 💰 Finans (1)

| Uygulama | Açıklama |
|----------|----------|
| 🪙 **Kripto Ticker** | CoinGecko API üzerinden BTC, ETH, SOL fiyatlarını çeker. 24 saatlik değişim yüzdesi ve trend okları |

---

### 🧊 Grafik Motorları (2)

| Uygulama | Açıklama |
|----------|----------|
| 🧊 **3D Küp** | Tel kafes küp (wireframe). Üç eksen etrafında otomatik döndürme, perspektif projeksiyon, vertex noktaları |
| 🌀 **Mandelbrot Fraktal** | Mandelbrot kümesi gezgini. UP/DOWN ile zoom in/out. İterasyon derinliği dinamik olarak ayarlanır |

---

### 🔧 Akıllı Araçlar (4)

| Uygulama | Açıklama |
|----------|----------|
| 📱 **QR Kod** | Cihazın IP adresini QR koda çevirir. Telefonla tarayarak Pi'ye tarayıcıdan erişim |
| 🐙 **GitHub** | GitHub katkı ızgarası, streak ve commit sayısı gösterimi |
| 🚀 **Speedtest** | İnternet hız testi. Analog kadran (speedometer) tarzı ibreli gösterim |
| 📰 **HackerNews** | Popüler HackerNews başlıklarını listeler. Seçilen haberin URL'si QR koda dönüşür |

---

### 🌡️ Sensörler (4)

| Uygulama | Açıklama |
|----------|----------|
| 🌡️ **Sıcaklık/Nem** | DHT11/DHT22 sensöründen oda sıcaklığı ve nem yüzdesi. Progress bar ve kritik sıcaklık uyarısı |
| 🔋 **UPS Pil** | UPS HAT üzerinden pil voltajı ve yüzdesini büyük pil görseli olarak çizer |
| 🪴 **Bitki Bakım** | Toprak nem sensörü ile bitkinin susuzluk seviyesini izler. GPIO röle ile otomatik sulama |
| 🧭 **Pusula** | HMC5883L manyetometre ile yön bilgisi. Dönen kadran üzerinde N/G/D/B yönleri |

---

### 🎵 Medya (3)

| Uygulama | Açıklama |
|----------|----------|
| 🎵 **MP3 Çalar** | `/home/pi/Music/` dizinindeki MP3 dosyalarını tarar ve `mpv` ile çalar. Otomatik sonraki parça, oynat/duraklat |
| 📻 **İnternet Radyo** | TRT FM, Jazz FM, LoFi HipHop ve Klasik müzik istasyonlarını `mpv` ile stream eder |
| 🎬 **Video Player** | Bad Apple!! tarzı 1-bit video oynatıcı. RLE sıkıştırılmış kare desteği, progress bar |

---

### 💬 Mesajlaşma (2)

| Uygulama | Açıklama |
|----------|----------|
| ✈️ **Telegram** | Telegram Bot API ile gelen mesajları listeler. Hazır yanıtlar gönderme |
| 📧 **Email** | IMAP üzerinden okunmamış e-posta sayısını büyük rakamlarla gösterir |

---

### 🌙 Astronomi (2)

| Uygulama | Açıklama |
|----------|----------|
| 🌙 **Ay Evresi** | Sinodik ay döngüsü hesabıyla Ay'ın o anki evresini (Yeni Ay → Dolunay) grafiksel olarak çizer. İnternet gerektirmez — saf trigonometri |
| 🌍 **Dünya Saati** | İstanbul, Londra, New York, Tokyo, Sydney saatlerini yan yana karşılaştırmalı gösterir |

---

### 🎨 Yaratıcı (2)

| Uygulama | Açıklama |
|----------|----------|
| 🎨 **Pixel Art** | OLED ekranı tuval olarak kullanarak piksel piksel çizim. Hareket ve çizim modları. Yanıp sönen imleç |
| 📸 **Screenshot** | OLED ekranın anlık görüntüsünü dosyaya kaydeder |

---

### 💪 Sağlık & Fitness (3)

| Uygulama | Açıklama |
|----------|----------|
| 🍅 **Pomodoro** | 25 dakika çalışma + 5 dakika mola döngüsü. Oturum sayacı, bildirimli geçişler |
| 🧘 **Nefes Egzersizi** | 4-7-8 nefes tekniği rehberi. Nefes fazına göre büyüyüp küçülen daire animasyonu |
| 🏋️ **HIIT Timer** | Tabata (20s/10s), HIIT (30s/15s), Custom egzersiz zamanlayıcı. Çalışma fazında ekran tam ters çevrilir |

---

### 🤖 Robotik (2)

| Uygulama | Açıklama |
|----------|----------|
| 🦾 **Servo Kontrol** | Yarım daire kadranla servo motor açısını (0°-180°) ayarlar. GPIO 18 PWM çıkışı |
| 🚗 **Robot Araba** | L298N motor sürücüyle ileri/geri/sol/sağ yön komutları. Hız göstergesi |

---

### 🌐 Ağ (2)

| Uygulama | Açıklama |
|----------|----------|
| 🕳️ **Pi-hole** | Engellenen reklam sayısı, DNS sorgu istatistikleri. Etkinleştir/devre dışı bırak toggle |
| 📹 **IP Kamera** | HTTP üzerinden JPEG frame yakalar ve 1-bit dithering ile OLED'de gösterir |

---

### 🎙️ Ses & 🔧 Bakım (4)

| Uygulama | Açıklama |
|----------|----------|
| 🎙️ **Sesli Kontrol** | Vosk offline konuşma tanıma motoru ile sesli komut. Ses dalgası animasyonu |
| 💾 **SD Kart Sağlık** | SD kartın toplam/kullanılan/boş alan bilgisi. Doluluk %90'ı aştığında uyarı |
| 📦 **APT Güncelleme** | Bekleyen paket güncellemelerini sayar ve listeler |
| ☑️ **Görev Listesi** | JSON tabanlı checklist. Tamamlama toggle, ilerleme sayacı |

---

## 🏗️ Mimari

### Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                              │
│                     (Giriş Noktası)                         │
├────────────────────────┬────────────────────────────────────┤
│                        │                                    │
│    ┌──────────────┐   │   ┌──────────────────────────┐     │
│    │  core/        │   │   │  desktop/                │     │
│    │  ┌──────────┐ │   │   │  ┌──────────────────┐   │     │
│    │  │ display  │─┤───┤───│  │ shell.py         │   │     │
│    │  │ (I2C)    │ │   │   │  │ (Durum Makinesi) │   │     │
│    │  └──────────┘ │   │   │  └──────────────────┘   │     │
│    │  ┌──────────┐ │   │   │  ┌────────┐ ┌────────┐ │     │
│    │  │framebuffer│ │   │   │  │launcher│ │statusbar│ │     │
│    │  │ (1024B)  │ │   │   │  │(10 pgs)│ │ (10px) │ │     │
│    │  └──────────┘ │   │   │  └────────┘ └────────┘ │     │
│    │  ┌──────────┐ │   │   │  ┌─────────────────┐   │     │
│    │  │  font    │ │   │   │  │ notification    │   │     │
│    │  │(5×7+8×8) │ │   │   │  │ (alt şerit)    │   │     │
│    │  └──────────┘ │   │   │  └─────────────────┘   │     │
│    │  ┌──────────┐ │   │   └──────────────────────────┘     │
│    │  │  input   │ │   │                                    │
│    │  │(3 düğme) │ │   │   ┌──────────────────────────┐     │
│    │  └──────────┘ │   │   │  apps/ (57 uygulama)     │     │
│    │  ┌──────────┐ │   │   │  snake, flappy, totp,    │     │
│    │  │scheduler │ │   │   │  mp3player, moon, ...    │     │
│    │  │(kooperatif)│ │  │   └──────────────────────────┘     │
│    │  └──────────┘ │   │                                    │
│    └──────────────┘   │                                    │
├────────────────────────┴────────────────────────────────────┤
│                    SSD1306 OLED (I2C)                       │
│                    128×64 piksel, 1-bit                     │
└─────────────────────────────────────────────────────────────┘
```

### Durum Makinesi

```
        ┌──────────┐
        │  SPLASH  │  (2 saniye açılış animasyonu)
        └────┬─────┘
             │ timeout
             ▼
        ┌──────────┐  SEL (uygulama seç)  ┌──────────┐
        │   HOME   │────────────────────▶│   APP    │
        │(Launcher)│◀────────────────────│ (Aktif)  │
        └──────────┘  LONG (geri dön)     └──────────┘
```

### Uygulama Arayüz Sözleşmesi

Her uygulama aşağıdaki standart arayüzü implemente eder:

```python
class MyApp:
    NAME  = "myapp"      # Benzersiz tanımlayıcı
    LABEL = "App"        # Launcher'da görünen isim (max 5 karakter)
    ICON  = "icon_name"  # font.py'deki 8×8 ikon adı

    def __init__(self, on_exit):
        self.on_exit = on_exit   # Ana menüye dönüş callback'i

    def on_up(self):    ...  # Yukarı düğme
    def on_down(self):  ...  # Aşağı düğme
    def on_sel(self):   ...  # Seç düğme
    def on_long(self):  ...  # Uzun basma (genelde: self.on_exit())

    def update(self):   ...  # Her tick'te çağrılır (veri güncelleme)
    def draw(self, fb):  ... # Her frame'de çağrılır (ekrana çizim)
```

### Framebuffer API

```python
fb.pixel(x, y, on=True)              # Tek piksel
fb.line(x0, y0, x1, y1)              # Bresenham çizgi
fb.rect(x, y, w, h, fill=False)      # Dikdörtgen
fb.circle(cx, cy, r, fill=False)     # Orta nokta daire
fb.rounded_rect(x, y, w, h, r=2)    # Yuvarlatılmış dikdörtgen
fb.text(string, x, y, on=True)       # 5×7 font metin
fb.text_centered(string, y)          # Yatay ortalı metin
fb.icon(name, x, y)                  # 8×8 ikon
fb.hline(x, y, w)                    # Yatay çizgi
fb.vline(x, y, h)                    # Dikey çizgi
fb.progress_bar(x, y, w, h, val, max_val=100)  # İlerleme çubuğu
```

---

## 📁 Dizin Yapısı

```
TinyOLED-Desktop/
├── main.py                  # Giriş noktası — config yükle, I2C bağlan, Desktop başlat
├── install.sh               # Tek adımda otomatik kurulum scripti
├── README.md                # Bu dosya
│
├── core/                    # Çekirdek motor modülleri
│   ├── display.py           # SSD1306 I2C düşük seviye sürücüsü
│   ├── framebuffer.py       # 128×64 sanal framebuffer + çizim primitifleri
│   ├── font.py              # 5×7 ASCII font (95 karakter) + 55+ 8×8 ikon
│   ├── input.py             # GPIO düğme yöneticisi (debounce + uzun basma)
│   └── scheduler.py         # Kooperatif görev zamanlayıcısı (tick tabanlı)
│
├── desktop/                 # Masaüstü kabuğu
│   ├── shell.py             # Ana durum makinesi (SPLASH → HOME → APP)
│   ├── statusbar.py         # Üst durum çubuğu (saat, WiFi, pil)
│   ├── launcher.py          # 3×2 ikon ızgarası, 10 sayfa, animasyonlu seçim
│   └── notification.py      # Alt bildirim şeridi (progress bar'lı)
│
├── apps/                    # 57 uygulama (her biri bağımsız modül)
│   ├── clock.py             # 🕐 Saat & Tarih
│   ├── sysinfo.py           # 💻 Sistem Bilgisi
│   ├── wifi.py              # 📡 WiFi Yöneticisi
│   ├── filebrowser.py       # 📁 Dosya Tarayıcı
│   ├── settings.py          # ⚙️ Ayarlar
│   ├── power.py             # ⏻ Güç Yönetimi
│   ├── snake.py             # 🐍 Yılan Oyunu
│   ├── flappy.py            # 🐦 Flappy Bird
│   ├── tamagotchi.py        # 🐾 Sanal Evcil Hayvan
│   ├── dice.py              # 🎲 Zar Simülatörü
│   ├── graph.py             # 📊 Gerçek Zamanlı Grafik
│   ├── docker_mon.py        # 🐳 Docker Monitör
│   ├── systemd_mon.py       # 🔄 Systemd Yöneticisi
│   ├── gpio_viewer.py       # 📌 GPIO Pin Viewer
│   ├── i2c_scan.py          # 🔍 I2C Bus Scanner
│   ├── script_runner.py     # 📜 Bash Komut Çalıştırıcı
│   ├── oscilloscope.py      # 📡 Mini Osiloskop
│   ├── multimeter.py        # ⚡ Dijital Multimetre
│   ├── ssh_alert.py         # 🛡️ SSH Saldırı Dedektörü
│   ├── totp.py              # 🔑 TOTP 2FA Authenticator
│   ├── passgen.py           # 🔒 Şifre Üreteci
│   ├── wifi_scan.py         # 📡 WiFi Ağ Tarayıcı
│   ├── ss_starfield.py      # ⭐ Starfield Screensaver
│   ├── ss_gameoflife.py     # 🧬 Game of Life
│   ├── ss_dvd.py            # 📀 DVD Bouncing Logo
│   ├── ss_matrix.py         # 💚 Matrix Digital Rain
│   ├── crypto.py            # 🪙 Kripto Para Ticker
│   ├── cube3d.py            # 🧊 3D Tel Kafes Küp
│   ├── fractal.py           # 🌀 Mandelbrot Fraktal
│   ├── qrcode_gen.py        # 📱 QR Kod Üreteci
│   ├── github_tracker.py    # 🐙 GitHub Tracker
│   ├── speedtest_app.py     # 🚀 Speedtest Kadranı
│   ├── hackernews.py        # 📰 HackerNews Okuyucu
│   ├── sensors.py           # 🌡️ Sıcaklık/Nem İstasyonu
│   ├── ups_battery.py       # 🔋 UPS Pil Durumu
│   ├── plant_monitor.py     # 🪴 Bitki Sulama Monitörü
│   ├── compass.py           # 🧭 Dijital Pusula
│   ├── mp3player.py         # 🎵 SD Kart MP3 Çalar
│   ├── radio.py             # 📻 İnternet Radyo
│   ├── videoplayer.py       # 🎬 1-bit Video Player
│   ├── telegram_bot.py      # ✈️ Telegram Bot
│   ├── email_counter.py     # 📧 Email Sayacı
│   ├── moon.py              # 🌙 Ay Evresi Göstergesi
│   ├── worldclock.py        # 🌍 Dünya Saati
│   ├── pixelart.py          # 🎨 Pixel Art Editörü
│   ├── screenshot.py        # 📸 Ekran Görüntüsü
│   ├── pomodoro.py          # 🍅 Pomodoro Timer
│   ├── breathing.py         # 🧘 Nefes Egzersizi
│   ├── workout.py           # 🏋️ HIIT/Tabata Timer
│   ├── servo.py             # 🦾 Servo Motor Kontrolü
│   ├── rc_car.py            # 🚗 Robot Araba Kumandası
│   ├── pihole.py            # 🕳️ Pi-hole Dashboard
│   ├── ipcam.py             # 📹 IP Kamera
│   ├── voice.py             # 🎙️ Sesli Kontrol
│   ├── sd_health.py         # 💾 SD Kart Sağlığı
│   ├── apt_update.py        # 📦 APT Güncelleme
│   └── todo.py              # ☑️ Görev Listesi
│
├── web-simulator/           # 🌐 Tarayıcı tabanlı OLED simülatörü
│   ├── index.html           # Ana sayfa (PCB board + OLED canvas)
│   ├── index.css            # Premium koyu tema stiller
│   ├── main.js              # Giriş noktası
│   └── js/                  # JavaScript motor portları
│       ├── framebuffer.js   # 128×64 software framebuffer
│       ├── font.js          # 5×7 font + 55 ikon (Python portu)
│       ├── display.js       # Canvas OLED renderer (glow efekti)
│       ├── input.js         # Klavye + dokunmatik düğmeler
│       ├── scheduler.js     # Kooperatif zamanlayıcı
│       ├── shell.js         # SPLASH → HOME → APP durum makinesi
│       ├── statusbar.js     # Üst durum çubuğu
│       ├── launcher.js      # 3×2 ikon ızgarası launcher
│       ├── notification.js  # Bildirim sistemi
│       └── apps/            # 15 port edilmiş uygulama
│           ├── clock.js     # 🕐 Saat (analog+dijital)
│           ├── snake.js     # 🐍 Yılan Oyunu
│           ├── flappy.js    # 🐦 Flappy Bird
│           ├── cube3d.js    # 🧊 3D Küp
│           ├── fractal.js   # 🌀 Mandelbrot Fraktal
│           └── ...          # +10 uygulama daha
│
├── config/
│   ├── config.json          # Ana yapılandırma dosyası
│   └── commands.json        # Script runner komut listesi
│
└── service/
    └── tinyoled.service     # Systemd servis dosyası
```

---

## ⚙️ Yapılandırma

`config/config.json` dosyası tüm sistem ayarlarını içerir:

```json
{
  "brightness": 200,
  "timeout_s": 60,
  "contrast": 2,
  "fps": 20,
  "i2c_bus": 1,
  "i2c_address": "0x3C",
  "pin_up": 17,
  "pin_down": 27,
  "pin_sel": 22,
  "start_dir": "/home/pi",
  "display_width": 128,
  "display_height": 64,
  "music_dir": "/home/pi/Music",
  "screensaver": "starfield",
  "screensaver_timeout_s": 120,
  "github_user": "",
  "telegram_token": "",
  "pihole_url": "http://localhost/admin/api.php",
  "ipcam_url": "http://192.168.1.100/capture"
}
```

| Anahtar | Açıklama | Varsayılan |
|---------|----------|-----------|
| `brightness` | OLED parlaklığı (0-255) | `200` |
| `fps` | Hedef kare hızı | `20` |
| `pin_up/down/sel` | GPIO pin numaraları | `17, 27, 22` |
| `music_dir` | MP3 dosyalarının dizini | `/home/pi/Music` |
| `screensaver` | Varsayılan ekran koruyucu | `starfield` |
| `screensaver_timeout_s` | Ekran koruyucu başlama süresi | `120` |
| `telegram_token` | Telegram Bot API token | `""` |
| `pihole_url` | Pi-hole API adresi | `http://localhost/admin/api.php` |

---

## 🧩 Kendi Uygulamanızı Yazın

Yeni bir uygulama eklemek sadece 3 adımdır:

### 1. Uygulama dosyasını oluşturun

```python
# apps/my_app.py
from core.framebuffer import Framebuffer

class MyApp:
    NAME  = "myapp"
    LABEL = "App"      # Max 5 karakter
    ICON  = "heart"    # font.py'deki ikon adı

    def __init__(self, on_exit):
        self.on_exit = on_exit
        self.counter = 0

    def on_up(self):    self.counter += 1
    def on_down(self):  self.counter -= 1
    def on_sel(self):   self.counter = 0
    def on_long(self):  self.on_exit()

    def update(self):   pass

    def draw(self, fb: Framebuffer):
        fb.text_centered("Benim Uygulamam", 14)
        fb.text_centered(f"Sayac: {self.counter}", 32)
        fb.text_centered("[UP/DN] Degistir", 50)
```

### 2. shell.py'ye kaydedin

```python
# desktop/shell.py → _register_apps() içine ekleyin:
from apps.my_app import MyApp
self._launcher.register("myapp", "App", "heart", lambda: self._open(MyApp(ex)))
```

### 3. (Opsiyonel) Özel ikon ekleyin

```python
# core/font.py → _ICONS_8X8 sözlüğüne ekleyin:
'my_icon': [
    0b00000000,
    0b01100110,
    0b11111111,
    0b11111111,
    0b01111110,
    0b00111100,
    0b00011000,
    0b00000000,
],
```

---

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-uygulama`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni uygulama: Hesap Makinesi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-uygulama`)
5. Pull Request açın

### Katkı Kuralları

- Her uygulama tek bir dosyada olmalıdır (`apps/uygulama.py`)
- Standart arayüz sözleşmesine uyulmalıdır (`on_up`, `on_down`, `on_sel`, `on_long`, `update`, `draw`)
- Harici donanım gerektiren uygulamalar, donanım yokken simülasyon/mock modunda çalışmalıdır
- Tüm metinler 128 piksel genişliğe sığmalıdır (max ~21 karakter)

---

## 📄 Lisans

**Tüm Hakları Saklıdır.** Bu proje özel bir lisans altında yayınlanmıştır. Kaynak kodu yalnızca görüntüleme ve eğitim amaçlı paylaşılmaktadır. Kopyalama, dağıtma, değiştirme veya ticari kullanım **yasaktır**. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

- [Raspberry Pi Foundation](https://www.raspberrypi.org/) — Raspberry Pi donanımı
- [Solomon Systech](https://www.solomon-systech.com/) — SSD1306 OLED sürücü çipi
- [Conway](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) — Game of Life hücresel otomatı
- [CoinGecko](https://www.coingecko.com/) — Kripto para fiyat API'si
- [Vosk](https://alphacephei.com/vosk/) — Offline konuşma tanıma

---

<p align="center">
  <strong>128 piksel ile neler yapılabileceğini keşfedin.</strong><br>
  <em>Crafted with ❤️ for the Raspberry Pi community</em>
</p>
