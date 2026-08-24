# Release Readiness

TinyOLED Desktop is a strong `v1.0.0` candidate because it has a clear product boundary, hardware path and browser simulator. Publish the tag only after every release-blocking check below is green.

## v1.0.0 gate

- [x] Portfolio README is concise and reproducible.
- [x] Live browser simulator is documented.
- [x] GitHub Pages deployment workflow exists.
- [x] GitHub Pages routing compatibility is fixed for both branch-source and Actions deployment modes.
- [x] Root `index.html` routes `/TinyOLED-Desktop/` to the simulator when branch-source Pages is used.
- [x] Pages workflow supports both `master` and `main` during the branch migration.
- [x] `main` is the GitHub default branch.
- [x] `main` and `master` histories were unified without force-push using merge commit `7ed7b7b128b2d74e0ad96233f1d6fd8befb81710`.
- [x] 57 / 57 browser launcher registrations are enforced in CI.
- [x] The 42 extended simulator applications are individual JavaScript modules; the generic `CatalogApp` placeholder is retired.
- [x] Browser implementation modes and security boundaries are documented.
- [x] Optional local Raspberry Pi bridge is loopback-bound, allow-listed and control-off by default.
- [x] Known limitations are documented.
- [x] `v1.0.0` release notes draft exists.
- [x] Static CI validated green against the current runtime/code tree via temporary PR CI run #28 (`32745087198`).
- [ ] Pages workflow confirmed green from `main`.
- [ ] Raspberry Pi + SSD1306 install path smoke-tested on the final release commit.
- [ ] Hardware-dependent BRG execution paths smoke-tested on the intended Raspberry Pi configuration.
- [ ] Release commit SHA locked below.

## CI evidence

Temporary validation PR #1 changed only `docs/CI_VALIDATION_MARKER.md`; runtime code was identical to its `main` base. GitHub Actions run #28 completed successfully with every release CI step green:

- Python syntax + `web-bridge/server.py` compile
- installer shell syntax
- device application inventory
- 57-app browser parity
- browser simulator contract
- JavaScript syntax across the simulator tree
- 42-module ESM export smoke test

The validation PR was closed without merging.

## Current integration candidate

`828dc0b75e044203ce4d0d95cad567cd4429edca`

This commit contains the post-merge Pages deployment marker on top of the 42-app browser runtime upgrade. Subsequent commits only update release-readiness documentation. It is **not** the final release SHA until Pages and hardware gates pass.

## Release commit

`NOT_LOCKED`

Replace this value with the final immutable commit SHA only after the remaining gates pass. The `v1.0.0` tag must point to that exact commit.

## Release notes

Draft: [`docs/RELEASE_NOTES_v1.0.0_DRAFT.md`](docs/RELEASE_NOTES_v1.0.0_DRAFT.md)

The final release notes must include:

- Raspberry Pi / SSD1306 hardware requirements,
- three-button interaction model,
- 57-application scope,
- browser simulator link,
- 42 application-specific browser implementations,
- `WEB` / `NET` / `SER` / `BRG` execution semantics,
- optional local bridge security boundary,
- install command,
- optional sensor/hardware dependencies,
- license terms,
- and a clear distinction between simulator-verified and hardware-verified behavior.

## Rule

Do not publish `v1.0.0` while any unchecked item above remains. A green browser deployment alone is not evidence that GPIO, I2C, Linux service control or optional peripheral behavior has been physically validated.
