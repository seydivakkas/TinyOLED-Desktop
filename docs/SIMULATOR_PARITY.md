# TinyOLED Desktop — Simulator Parity

## Current state

- Device-side Raspberry Pi / SSD1306 catalog: **57 applications**
- Browser launcher registrations: **57**
- Original standalone JavaScript applications: **15**
- Newly upgraded individual JavaScript modules: **42**
- Generic placeholder application classes used by the 42: **0**

The 42 extended applications are exported through `web-simulator/js/apps/extended_apps.js`, but each implementation lives in its own module.

## What “57 / 57” means

Every documented device application has a browser launcher entry and an application-specific JavaScript implementation surface.

It does **not** mean a GitHub Pages tab can directly perform privileged Linux operations or prove physical sensor/GPIO behavior.

## Execution model

### WEB

Browser-native behavior:

- local/session storage
- Web Crypto
- File System Access
- MediaDevices
- Web Audio
- Speech Recognition where supported
- DeviceOrientation
- Battery / Wake Lock where supported
- StorageManager
- Canvas download and media processing
- `Intl.DateTimeFormat`

### NET

Public network APIs / streams:

- CoinGecko
- GitHub REST API
- Hacker News Firebase API
- internet radio streams
- optional measured download attempt for Speedtest

Network failures, rate limits and CORS are surfaced as errors; success is never fabricated.

### SER

Hardware adapters may use Web Serial with newline-delimited JSON commands.

Examples:

```json
{"cmd":"i2c.scan","bus":1}
{"cmd":"ina219.read"}
{"cmd":"servo.write","pin":18,"angle":90}
{"cmd":"car.drive","direction":"stop","speed":0}
```

### BRG

Linux/service/private-credential operations use the optional local bridge in `web-bridge/server.py`.

The bridge:

- binds to loopback by default,
- uses explicit endpoint allow-lists,
- rejects arbitrary shell text,
- stores no secret in the client bundle,
- keeps mutating actions disabled unless `TINY_ALLOW_CONTROL=1`.

## Security boundary

Browser source code must never contain:

- e-mail passwords,
- Telegram bot tokens,
- WiFi credentials,
- TOTP seed values,
- shell command text supplied by remote users.

TOTP secrets are session-only. WiFi passwords are sent only to a user-configured local bridge and are not stored by the web app.

## Verification

CI checks:

1. 57 launcher registrations.
2. Exactly 42 individual extended application modules.
3. Exactly 42 exports from the barrel module.
4. No dependency on the retired generic `CatalogApp` placeholder.
5. JavaScript syntax for every simulator module.
6. Successful ESM import of all 42 extended classes.
7. Python syntax for `web-bridge/server.py`.

See [BROWSER_APP_MATRIX.md](BROWSER_APP_MATRIX.md) for the one-by-one implementation map.
