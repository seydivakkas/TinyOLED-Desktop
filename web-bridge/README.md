# TinyOLED Local Browser Bridge

The public GitHub Pages simulator cannot directly access Linux services, Raspberry Pi GPIO/I2C or private credentials. `web-bridge/server.py` is an **optional local companion** for those features.

## Safe default

```bash
python3 web-bridge/server.py
```

The bridge binds to `127.0.0.1:8765` and privileged mutations are **disabled**.

For control operations:

```bash
TINY_ALLOW_CONTROL=1 python3 web-bridge/server.py
```

Only explicit allow-listed actions are accepted. The bridge never accepts arbitrary shell commands from the web UI.

## Public GitHub Pages + Raspberry Pi

A practical secure route is an SSH tunnel:

```bash
ssh -L 8765:127.0.0.1:8765 pi@raspberrypi.local
```

Then set the simulator bridge URL to:

```text
http://127.0.0.1:8765
```

## Optional secrets

Keep these only in the Pi process environment:

```bash
export TINY_EMAIL_HOST=imap.example.com
export TINY_EMAIL_USER=user@example.com
export TINY_EMAIL_PASSWORD='...'
export TINY_TELEGRAM_BOT_TOKEN='...'
```

No password/token belongs in the GitHub repository or client-side JavaScript.

## Serial JSON protocol

Hardware-facing JavaScript applications first try Web Serial when supported. A serial endpoint may answer newline-delimited JSON commands such as:

```json
{"cmd":"i2c.scan","bus":1}
{"cmd":"ina219.read"}
{"cmd":"servo.write","pin":18,"angle":90}
{"cmd":"car.drive","direction":"stop","speed":0}
```

If Web Serial is unavailable or fails, the browser falls back to `POST /api/io` on this bridge.

## Control policy

Mutating endpoints remain disabled unless `TINY_ALLOW_CONTROL=1`:

- WiFi connect
- Docker start/stop
- systemd restart
- poweroff/reboot
- GPIO write
- pump control
- servo commands
- robot-car commands
- Pi-hole enable/disable

Read-only diagnostics can run in default mode.
