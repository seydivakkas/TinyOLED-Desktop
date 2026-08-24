# TinyOLED Desktop — Simulator Parity

The Raspberry Pi / SSD1306 application catalog contains **57 device-side applications**. The static GitHub Pages simulator currently contains **15 JavaScript ports**.

This is intentional architecture, not automatic code sharing: the device applications are Python modules with access to Linux, GPIO, I2C, local files, sensors, subprocesses and credentials, while GitHub Pages is a sandboxed static browser environment.

## Current parity

### Ported to the browser — 15

- Clock
- System Info
- Snake
- Flappy Bird
- Dice
- 3D Cube
- Mandelbrot Fractal
- Breathing Exercise
- Pomodoro
- Moon Phase
- Starfield
- Matrix Rain
- Game of Life
- DVD Logo
- Settings

## Why the remaining applications are not automatic ports

### A. Browser-native / straightforward simulation candidates

These can be ported with little or no device emulation:

- Tamagotchi
- Real-time Graph (using synthetic/browser metrics)
- Password Generator
- World Clock
- Pixel Art
- HIIT Timer
- QR Code
- Screenshot

### B. Network-backed applications

These can be represented in the browser, but real data depends on public APIs, CORS policy, rate limits or credentials:

- Crypto Ticker
- GitHub Tracker
- HackerNews
- Speedtest
- Internet Radio
- IP Camera
- Telegram
- E-mail

For a public GitHub Pages demo, no private token or account credential should be embedded in client-side JavaScript.

### C. Raspberry Pi / Linux integration applications

These depend on operating-system facilities unavailable to a static web page. The browser version should use a mock or recorded-data adapter instead of pretending to execute the real action:

- WiFi Manager / WiFi Scanner
- File Browser
- Power Manager
- Docker Monitor
- systemd Manager
- SSH Alert
- Command Runner
- Pi-hole
- SD Card Health
- APT Update
- MP3 Player (device-local library)
- Video Player (device-local / RLE pipeline)

### D. Hardware / sensor applications

These require real GPIO, I2C, ADC, PWM or attached peripherals on the Raspberry Pi. A browser simulator can reproduce the screen and state transitions, but not the physical measurement/control path without an external bridge:

- GPIO Viewer
- I2C Scanner
- Oscilloscope / MCP3008
- Multimeter / INA219
- Temperature / Humidity
- UPS Battery
- Plant Monitor
- Compass / HMC5883L
- Servo Control
- Robot Car / L298N

### E. Browser-adaptable with a different implementation

These can be simulated, but the web implementation should use browser APIs rather than copy the Python/Linux implementation literally:

- TOTP 2FA — Web Crypto / pure JS implementation; never ship real secrets in the repository
- Voice Control — Web Speech API or microphone-based demo where supported
- MP3 / Radio — HTML5 Audio
- Camera — browser/media or safe sample frames

## Parity policy

Every simulator application should be marked as one of:

- `PORT` — behavior implemented directly in JavaScript
- `MOCK` — UI/state behavior reproduced using deterministic synthetic or recorded data
- `BRIDGE` — requires a Raspberry Pi/local backend to provide real hardware or OS data

The public GitHub Pages simulator must never claim hardware validation when it is displaying mock data.

## Recommended implementation order

### Phase 1 — 15 → 25

Add browser-native applications first:

1. Tamagotchi
2. Password Generator
3. World Clock
4. HIIT Timer
5. Pixel Art
6. QR Code
7. Screenshot
8. Real-time Graph
9. Crypto Ticker demo
10. GitHub Tracker demo

### Phase 2 — 25 → 40

Add deterministic mocks for Linux/network/device functions:

- WiFi
- File Browser
- Power
- Docker
- systemd
- SSH Alert
- I2C Scanner
- GPIO Viewer
- Sensor dashboard
- SD Health
- Pi-hole
- HackerNews
- Speedtest
- APT Update
- Command Runner

### Phase 3 — 40 → 57

Complete the remaining media, communication, robotics and sensor screens with explicit `MOCK` / `BRIDGE` labels.

## Release gate

Do not describe the browser simulator as **57-app parity** until all 57 launcher entries have a defined `PORT`, `MOCK` or `BRIDGE` implementation and the parity inventory is automatically checked in CI.
