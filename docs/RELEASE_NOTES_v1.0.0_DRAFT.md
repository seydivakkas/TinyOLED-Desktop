# TinyOLED Desktop v1.0.0 — Release Notes Draft

> Status: release candidate documentation only. Do not publish the tag until `RELEASE_READINESS.md` is fully green.

## Overview

TinyOLED Desktop is a framebuffer-first micro desktop for Raspberry Pi and a 128×64 SSD1306 OLED. It provides a compact application environment controlled with three physical buttons and includes a browser simulator for hardware-independent inspection.

## Highlights

- Custom monochrome framebuffer rendering stack
- 5×7 bitmap font renderer and compact icon system
- Cooperative application scheduling and explicit UI state handling
- 57+ documented applications across utilities, monitoring, visualization and games
- Raspberry Pi + SSD1306 I2C hardware path
- Three-button interaction model
- Browser-based simulator deployed with GitHub Pages
- Systemd service integration for boot-time startup
- Release-readiness CI for Python syntax, installer syntax and simulator contracts

## Quick start

```bash
git clone https://github.com/seydivakkas/TinyOLED-Desktop.git
cd TinyOLED-Desktop
sudo bash install.sh
sudo reboot
```

After installation, verify the SSD1306 is visible on the expected I2C bus before treating the hardware path as validated.

## Browser simulator

Public simulator:

https://seydivakkas.github.io/TinyOLED-Desktop/

The simulator demonstrates the desktop interaction model and application UI without requiring physical hardware. It does not emulate GPIO/I2C electrical behavior or all hardware-dependent application effects.

## Hardware scope

Core target:

- Raspberry Pi
- SSD1306 128×64 monochrome OLED
- I2C
- Three tactile buttons

Optional applications may additionally require sensors, ADCs, motor drivers, servo hardware, audio devices or network connectivity.

## Validation required before release

The final `v1.0.0` tag must point to a commit for which all of the following are recorded:

1. GitHub default branch is `main`.
2. Static CI is green on the release commit.
3. GitHub Pages deployment is green from `main`.
4. Raspberry Pi + SSD1306 installation smoke test passes.
5. Browser simulator and documented application inventory are checked for parity.
6. Release commit SHA is recorded in `RELEASE_READINESS.md`.

## Known limitations

See [`KNOWN_LIMITATIONS.md`](../KNOWN_LIMITATIONS.md).

The browser simulator is not a substitute for hardware validation. Some applications also require Linux utilities, elevated privileges, internet access or optional peripherals.

## License

Use and redistribution are governed by the repository `LICENSE` file. Release notes do not grant rights beyond that license.
