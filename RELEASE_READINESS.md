# Release Readiness

TinyOLED Desktop is a strong `v1.0.0` candidate because it has a clear product boundary, hardware path and browser simulator. Publish the tag only after the checks below are green.

## v1.0.0 gate

- [x] Portfolio README is concise and reproducible.
- [x] Live browser simulator is documented.
- [x] GitHub Pages deployment workflow exists.
- [x] `main` branch contains the current candidate content.
- [ ] GitHub default branch switched to `main`.
- [ ] Pages workflow confirmed green from `main`.
- [ ] Raspberry Pi + SSD1306 install path smoke-tested on the release commit.
- [ ] Browser simulator and hardware application catalog checked for version parity.
- [ ] Release commit SHA recorded.

## Release notes must include

- Raspberry Pi / SSD1306 hardware requirements,
- three-button interaction model,
- 57+ application scope,
- browser simulator link,
- install command,
- optional sensor/hardware dependencies,
- license terms.

The release should distinguish simulator-verified behavior from hardware-specific behavior where relevant.
