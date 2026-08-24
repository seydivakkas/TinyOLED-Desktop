# Release Readiness

TinyOLED Desktop is a strong `v1.0.0` candidate because it has a clear product boundary, hardware path and browser simulator. Publish the tag only after every release-blocking check below is green.

## v1.0.0 gate

- [x] Portfolio README is concise and reproducible.
- [x] Live browser simulator is documented.
- [x] GitHub Pages deployment workflow exists.
- [x] `main` branch contains the current candidate content.
- [x] Static release-readiness CI workflow exists and supports manual dispatch.
- [x] Known limitations are documented.
- [x] `v1.0.0` release notes draft exists.
- [ ] GitHub default branch switched to `main`.
- [ ] Static CI confirmed green on the release candidate commit.
- [ ] Pages workflow confirmed green from `main`.
- [ ] Raspberry Pi + SSD1306 install path smoke-tested on the release commit.
- [ ] Browser simulator and hardware application catalog checked for version parity.
- [ ] Release commit SHA recorded below.

## Release commit

`NOT_LOCKED`

Replace this value with the final immutable commit SHA only after the remaining gates pass. The `v1.0.0` tag must point to that exact commit.

## Release notes

Draft: [`docs/RELEASE_NOTES_v1.0.0_DRAFT.md`](docs/RELEASE_NOTES_v1.0.0_DRAFT.md)

The final release notes must include:

- Raspberry Pi / SSD1306 hardware requirements,
- three-button interaction model,
- 57+ application scope,
- browser simulator link,
- install command,
- optional sensor/hardware dependencies,
- license terms,
- and a clear distinction between simulator-verified and hardware-verified behavior.

## Rule

Do not publish `v1.0.0` while any unchecked item above remains. A green browser deployment alone is not evidence that GPIO, I2C or optional peripheral behavior has been validated.
