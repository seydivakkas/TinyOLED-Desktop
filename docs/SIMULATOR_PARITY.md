# TinyOLED Desktop — 57-App Web Simulator Parity

The Raspberry Pi / SSD1306 catalog contains **57 device-side applications**. The browser simulator now exposes **57 launcher entries** and JavaScript implementations for every catalog surface.

The implementations are intentionally classified by execution semantics:

- `PORT` — browser-native behavior implemented in JavaScript.
- `MOCK` — deterministic/safe demo behavior when real data would require credentials, CORS-sensitive services or machine-local resources.
- `BRIDGE` — the UI/state contract is ported, but real I/O requires Raspberry Pi/Linux/hardware access.

## What changed

The original simulator contained 15 standalone JavaScript applications. The remaining **42 applications** are now implemented as explicit JavaScript app classes through `web-simulator/js/apps/extended_apps.js`, backed by the shared `CatalogApp` interaction renderer.

The launcher registry in `web-simulator/js/shell.js` contains **57 entries**, matching the documented device catalog.

## Safety and claim boundary

GitHub Pages cannot directly provide Linux process control, GPIO, I2C, ADC/PWM, local `/var/log` access, Docker/systemd control, IMAP credentials, Telegram secrets or attached sensor readings. Those surfaces therefore do **not** pretend to execute real hardware actions in the public simulator.

A `BRIDGE` screen demonstrates the interaction and display contract that the device-side Python app uses. A future local bridge can replace demo state with real Raspberry Pi data without changing the launcher contract.

`MOCK` surfaces never embed private tokens or credentials in client-side JavaScript.

## 57-app launcher parity

The catalog now includes all documented families:

- System applications
- Games
- Monitoring & graphs
- Developer tools
- Security
- Screensavers
- Finance
- Graphics engines
- Smart tools
- Sensors
- Media
- Messaging
- Astronomy
- Creative tools
- Health & fitness
- Robotics
- Networking
- Voice & maintenance

## CI parity gate

`.github/workflows/ci.yml` now verifies:

1. the device-side Python application inventory remains intact,
2. exactly **57 browser launcher registrations** exist,
3. exactly **42 extended JavaScript app classes** exist in addition to the original 15 standalone browser apps,
4. the simulator page advertises `57 / 57 app`,
5. JavaScript syntax passes across the complete simulator tree.

The browser may be described as **57-app launcher parity** only while these checks remain green.

## Execution model

```text
Raspberry Pi / Python app               Browser representation
--------------------------              ----------------------
normal browser-safe behavior     --->   PORT
credential/network dependency    --->   MOCK
Linux/GPIO/I2C/sensor dependency --->   BRIDGE
```

This preserves portfolio honesty: visual and launcher parity is available for all 57 applications, while hardware validation remains explicitly separate.
