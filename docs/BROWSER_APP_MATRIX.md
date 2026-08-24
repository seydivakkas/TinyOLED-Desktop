# TinyOLED Desktop — Browser App Implementation Matrix

The web simulator exposes all **57 launcher entries**. The original 15 JavaScript applications remain standalone implementations. The other **42 applications are now individual JavaScript modules**, not generic placeholder screens.

## Execution modes

- **WEB** — uses browser APIs directly.
- **NET** — uses a public network API or media stream.
- **SER** — uses Web Serial when supported, with local bridge fallback.
- **BRG** — uses the optional local TinyOLED bridge for Raspberry Pi/Linux privileged operations.

No browser-only screen is presented as proof that physical GPIO, I2C, Linux service or sensor behavior has been validated.

## 42 upgraded applications

| # | Application | Module | Real browser behavior |
|---:|---|---|---|
| 1 | WiFi Manager | `wifi.js` | Network Information API + bridge scan/connect |
| 2 | File Browser | `filebrowser.js` | File System Access API directory navigation |
| 3 | Power | `power.js` | Battery API, Screen Wake Lock, optional Pi bridge power action |
| 4 | Tamagotchi | `tamagotchi.js` | Persistent state and time-based decay in localStorage |
| 5 | Real-time Graph | `graph.js` | Event-loop lag, JS heap and connection metrics |
| 6 | Docker Monitor | `docker.js` | Live container list/start/stop through local bridge |
| 7 | systemd Manager | `systemd.js` | Service state/restart through allow-listed bridge |
| 8 | GPIO Viewer | `gpio.js` | Web Serial JSON protocol with bridge fallback |
| 9 | I2C Scanner | `i2c.js` | Web Serial/bridge I2C scan |
| 10 | Command Runner | `command_runner.js` | Allow-listed diagnostic command IDs through bridge |
| 11 | Oscilloscope | `oscilloscope.js` | Microphone waveform via MediaDevices + Web Audio |
| 12 | Multimeter | `multimeter.js` | INA219 values through Web Serial/bridge |
| 13 | SSH Alert | `ssh_alert.js` | Live auth-log events through bridge |
| 14 | TOTP 2FA | `totp.js` | RFC 6238 HMAC-SHA1 via Web Crypto; secret is session-only |
| 15 | Password Generator | `password_generator.js` | Rejection-sampled Web Crypto random generation |
| 16 | WiFi Scanner | `wifi_scanner.js` | Real local scan through bridge |
| 17 | Crypto Ticker | `crypto.js` | CoinGecko public API |
| 18 | QR Code | `qr.js` | Real QR matrix generated in-browser with `qrcode` ESM |
| 19 | GitHub Tracker | `github_tracker.js` | GitHub public REST API |
| 20 | Speedtest | `speedtest.js` | Network Information API + measured download attempt |
| 21 | HackerNews | `hackernews.js` | Hacker News Firebase API |
| 22 | Temperature/Humidity | `temperature_humidity.js` | DHT data over Serial/bridge |
| 23 | UPS Battery | `ups_battery.js` | Browser Battery API + physical UPS bridge |
| 24 | Plant Monitor | `plant_monitor.js` | Moisture + pump state over Serial/bridge |
| 25 | Compass | `compass.js` | DeviceOrientation compass with HMC5883L fallback |
| 26 | MP3 Player | `mp3.js` | Local file picker + HTMLAudio playback/seek |
| 27 | Internet Radio | `radio.js` | HTMLAudio live internet streams |
| 28 | Video Player | `video.js` | Local video picker + 1-bit OLED frame conversion |
| 29 | Telegram | `telegram.js` | Server-side Bot API bridge; no token in client |
| 30 | E-mail | `email.js` | Server-side IMAP bridge; no password in client |
| 31 | World Clock | `world_clock.js` | Intl.DateTimeFormat timezone rendering |
| 32 | Pixel Art | `pixel_art.js` | Editable persistent OLED pixel grid |
| 33 | Screenshot | `screenshot.js` | Canvas PNG export/download |
| 34 | HIIT Timer | `hiit.js` | Real performance-clock interval state machine |
| 35 | Servo Control | `servo.js` | Web Serial/bridge angle command |
| 36 | Robot Car | `robot_car.js` | Web Serial/bridge drive commands + stop-on-exit |
| 37 | Pi-hole | `pihole.js` | Live statistics/control through bridge |
| 38 | IP Camera | `ipcam.js` | getUserMedia live camera + 1-bit dithering |
| 39 | Voice Control | `voice_control.js` | Web Speech Recognition API |
| 40 | SD Card Health | `sd_health.js` | StorageManager estimate + Pi storage bridge |
| 41 | APT Update | `apt_update.js` | Read-only package update inventory through bridge |
| 42 | Task List | `todo.js` | Persistent localStorage task state + add/toggle actions |

## Security contract

1. GitHub Pages never embeds e-mail, Telegram, WiFi or service credentials.
2. TOTP secrets are held in `sessionStorage`, not committed.
3. Command Runner sends an allow-listed command identifier, never arbitrary shell text.
4. Privileged Pi mutations belong in the local bridge and are disabled by default.
5. Camera, microphone, orientation, file and serial APIs always rely on browser permission prompts.
6. Network APIs may fail because of CORS, rate limits or connectivity; the UI surfaces failure rather than fabricating success.

## Parity definition

`57 / 57 launcher parity` means every device application now has a dedicated browser implementation surface. It does **not** mean Raspberry Pi hardware behavior has been verified from GitHub Pages.
