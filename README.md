<p align="center">
  <img src="docs/banner.png" alt="TinyOLED Desktop" width="640">
</p>

<div align="center">

# TinyOLED Desktop

### Framebuffer-First Micro Desktop for Raspberry Pi + SSD1306

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Embedded-A22846?style=flat-square&logo=raspberrypi&logoColor=white)
![SSD1306](https://img.shields.io/badge/OLED-128%C3%9764-0A66C2?style=flat-square)
![Python](https://img.shields.io/badge/Python-3-3776AB?style=flat-square&logo=python&logoColor=white)
![Device Apps](https://img.shields.io/badge/device%20apps-57-2EA44F?style=flat-square)
![Web Launcher](https://img.shields.io/badge/web%20launcher-57%2F57-2EA44F?style=flat-square)
[![Pages](https://github.com/seydivakkas/TinyOLED-Desktop/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/seydivakkas/TinyOLED-Desktop/actions/workflows/deploy-pages.yml)

**A tiny desktop environment built without a GUI framework: custom framebuffer rendering, bitmap fonts, monochrome icons, cooperative scheduling and a browser-based OLED simulator.**

`Embedded Systems` · `Framebuffer` · `Raspberry Pi` · `SSD1306` · `I²C` · `State Machines`

### **[Live Browser Simulator →](https://seydivakkas.github.io/TinyOLED-Desktop/)**

</div>

---

## Why this project matters

TinyOLED Desktop explores how much interface and application behavior can be built inside the constraints of a **128×64 monochrome display controlled with only three physical buttons**.

Instead of relying on a desktop GUI toolkit, the project implements the rendering and interaction stack directly. That makes it a compact systems project covering graphics primitives, input state, scheduling, memory constraints and embedded interaction design.

---

## Application scope

The Raspberry Pi / SSD1306 project contains a **57-application device catalog**. The browser simulator now exposes **57 / 57 launcher entries** and a JavaScript representation for every documented application surface.

The browser implementations are deliberately classified:

- **`WEB`** — browser-native JavaScript behavior.
- **`NET`** — public network API or media-stream behavior.
- **`SER`** — Web Serial hardware path with local bridge fallback where appropriate.
- **`BRG`** — real Linux/service/private-credential operations through the optional local Raspberry Pi bridge.

This distinction prevents browser state from being presented as proof of physical hardware validation.

**Current parity:** `57 / 57 browser launcher entries · 15 original standalone apps + 42 individual browser modules`

See **[Simulator Parity](docs/SIMULATOR_PARITY.md)** and **[Browser Implementation Matrix](docs/BROWSER_APP_IMPLEMENTATION.md)** for the execution model and claim boundary.

---

## Minimum reproducible run

### Browser path — no hardware required

Open the **[live simulator](https://seydivakkas.github.io/TinyOLED-Desktop/)** and navigate the 57-app launcher with the on-screen buttons or keyboard.

### Raspberry Pi path

```bash
git clone https://github.com/seydivakkas/TinyOLED-Desktop.git
cd TinyOLED-Desktop
sudo bash install.sh
sudo reboot
```

For manual hardware setup, enable I²C, verify the SSD1306 at address `0x3C`, then run:

```bash
sudo i2cdetect -y 1
sudo python3 main.py
```

For release-candidate hardware validation:

```bash
python3 tools/hardware_smoke_test.py
```

See **[Hardware Smoke Test](docs/HARDWARE_SMOKE_TEST.md)** for the read-only release procedure.

---

## Core architecture

```text
Physical Buttons / Browser Input
             ↓
        Input Manager
             ↓
     Desktop Shell State
   SPLASH → HOME → APP
             ↓
    Cooperative Scheduler
             ↓
      Application Layer
             ↓
 Custom Framebuffer Engine
   ├── 5×7 bitmap font
   ├── 8×8 icon system
   └── drawing primitives
             ↓
       SSD1306 128×64
```

The same interaction contract is mirrored in the browser. Device-specific integrations remain explicitly separated through `WEB`, `NET`, `SER` and `BRG` semantics.

---

## Engineering highlights

| Area | Implementation |
|---|---|
| Rendering | Custom monochrome framebuffer engine |
| Typography | 5×7 bitmap font renderer |
| Icons | Compact 8×8 monochrome icon set |
| Scheduling | Cooperative task / application scheduling |
| Navigation | Launcher, status bar, notifications and app lifecycle |
| Input | Three-button physical interaction model |
| Hardware | Raspberry Pi + SSD1306 over I²C |
| Simulation | Browser implementation of the OLED desktop behavior |
| Device application set | **57 applications** across utilities, visualization, games, sensors and system tools |
| Browser launcher parity | **57 / 57 entries** |
| Web implementation structure | **15 standalone apps + 42 individual browser modules** |
| Validation | CI parity/syntax/export gates + successful Pages deployment |

---

## Browser simulator

The GitHub Pages simulator includes the complete **57-entry application launcher**. Browser-safe applications use real browser APIs where possible; network applications use real public APIs/streams; hardware/Linux surfaces use Web Serial or the optional local bridge rather than pretending that browser-generated values are physical measurements.

CI enforces the 57 launcher registrations, the 42 individual extended modules, JavaScript syntax and ESM exports. The upgraded runtime has also completed a successful GitHub Pages deployment from `main`.

### **[Open the live simulator](https://seydivakkas.github.io/TinyOLED-Desktop/)**

### **[Simulator parity contract →](docs/SIMULATOR_PARITY.md)**

---

## Technology stack

`Python` · `Raspberry Pi` · `SSD1306` · `I²C` · `Framebuffer Rendering` · `Bitmap Fonts` · `State Machines` · `JavaScript` · `Canvas` · `Web APIs` · `Web Serial`

---

## Engineering principles

1. **Build the rendering primitive before the widget**
2. **Design for the physical display constraint**
3. **Keep interaction deterministic with explicit state machines**
4. **Separate application logic from the display backend**
5. **Do not present simulated data as hardware validation**
6. **Enforce device/browser catalog parity in CI**
7. **Keep privileged bridge operations explicit, local and opt-in**

---

## Documentation

- **[Full Technical Documentation](docs/README_FULL.md)**
- **[Simulator Parity](docs/SIMULATOR_PARITY.md)**
- **[Browser Implementation Matrix](docs/BROWSER_APP_IMPLEMENTATION.md)**
- **[Hardware Smoke Test](docs/HARDWARE_SMOKE_TEST.md)**
- **[Release Readiness](RELEASE_READINESS.md)**

---

<div align="center">

**128×64 pixels. Three buttons. 57 application surfaces.**

[Live Simulator](https://seydivakkas.github.io/TinyOLED-Desktop/) · [Simulator Parity](docs/SIMULATOR_PARITY.md) · [Hardware Smoke Test](docs/HARDWARE_SMOKE_TEST.md)

</div>
