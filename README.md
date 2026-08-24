<p align="center">
  <img src="docs/banner.png" alt="TinyOLED Desktop" width="640">
</p>

<div align="center">

# TinyOLED Desktop

### Framebuffer-First Micro Desktop for Raspberry Pi + SSD1306

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Embedded-A22846?style=flat-square&logo=raspberrypi&logoColor=white)
![SSD1306](https://img.shields.io/badge/OLED-128%C3%9764-0A66C2?style=flat-square)
![Python](https://img.shields.io/badge/Python-3-3776AB?style=flat-square&logo=python&logoColor=white)
![Apps](https://img.shields.io/badge/apps-57%2B-2EA44F?style=flat-square)
[![Pages](https://github.com/seydivakkas/TinyOLED-Desktop/actions/workflows/deploy-pages.yml/badge.svg?branch=main)](https://github.com/seydivakkas/TinyOLED-Desktop/actions/workflows/deploy-pages.yml)

**A tiny desktop environment built without a GUI framework: custom framebuffer rendering, bitmap fonts, monochrome icons, cooperative scheduling and a browser-based OLED simulator.**

`Embedded Systems` · `Framebuffer` · `Raspberry Pi` · `SSD1306` · `I²C` · `State Machines`

### **[Live Browser Simulator →](https://seydivakkas.github.io/TinyOLED-Desktop/)**

</div>

---

## Why this project matters

TinyOLED Desktop explores how much interface and application behavior can be built inside the constraints of a **128×64 monochrome display controlled with only three physical buttons**.

Instead of relying on a desktop GUI toolkit, the project implements the rendering and interaction stack directly. That makes it a compact systems project covering graphics primitives, input state, scheduling, memory constraints and embedded interaction design.

---

## Minimum reproducible run

### Browser path — no hardware required

Open the **[live simulator](https://seydivakkas.github.io/TinyOLED-Desktop/)** to inspect the framebuffer/UI behavior directly.

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

The same interaction model is mirrored in the browser simulator so the desktop can be explored without physical hardware.

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
| Application set | **57+ applications** across utilities, visualization, games and system tools |

---

## What it demonstrates

TinyOLED Desktop is intentionally different from the AI-heavy projects in this portfolio. It demonstrates lower-level engineering breadth:

- framebuffer graphics,
- constrained UI design,
- embedded state machines,
- physical input handling,
- cooperative scheduling,
- hardware / software boundaries,
- and cross-platform simulation of an embedded interface.

---

## Example application families

**System & utilities**  
Clock · system information · Wi-Fi tools · settings · file utilities · timers

**Visualization**  
Graphs · matrix effects · starfield · fractal / geometry demos

**Games & interaction**  
Snake · Flappy-style game · dice · virtual pet and other compact applications

**Productivity / ambient**  
Pomodoro · breathing tools · notifications · status views

---

## Browser simulator

The browser simulator reproduces the OLED interaction model using a canvas-based renderer and lets the project be evaluated without a Raspberry Pi or physical SSD1306 module.

### **[Open the live simulator](https://seydivakkas.github.io/TinyOLED-Desktop/)**

---

## Technology stack

`Python` · `Raspberry Pi` · `SSD1306` · `I²C` · `Framebuffer Rendering` · `Bitmap Fonts` · `State Machines` · `JavaScript / Canvas Simulator`

---

## Engineering principles

1. **Build the rendering primitive before the widget**
2. **Design for the physical display constraint**
3. **Keep interaction deterministic with explicit state machines**
4. **Separate application logic from the display backend**
5. **Provide a simulator so hardware-dependent work remains inspectable**

---

## Documentation

The root README is intentionally concise and portfolio-oriented. The original full project documentation is preserved here:

### **[Full Technical Documentation →](docs/README_FULL.md)**

It contains the full application catalog, hardware setup, architecture details, controls and implementation notes.

---

<div align="center">

**128×64 pixels. Three buttons. A complete micro-desktop experiment.**

[Live Simulator](https://seydivakkas.github.io/TinyOLED-Desktop/) · [GitHub Profile](https://github.com/seydivakkas) · [Full Documentation](docs/README_FULL.md)

</div>
