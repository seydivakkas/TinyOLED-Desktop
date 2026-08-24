# Raspberry Pi / SSD1306 Release Smoke Test

Use this checklist before locking the `v1.0.0` release SHA. The automated script is intentionally **read-only**: it does not toggle GPIO outputs, move a servo, drive motors, change WiFi, restart services or reboot/shutdown the Pi.

## 1. Install candidate

```bash
git clone https://github.com/seydivakkas/TinyOLED-Desktop.git
cd TinyOLED-Desktop
git checkout main
sudo bash install.sh
sudo reboot
```

After reboot:

```bash
cd /home/pi/tiny-oled-desktop
python3 tools/hardware_smoke_test.py
```

The script writes `hardware_smoke_report.json`, which is ignored by Git.

## 2. Required PASS conditions

For the core release path, verify:

- Linux platform detected.
- Raspberry Pi model detected.
- Python source compiles.
- `smbus2` is installed.
- `/dev/i2c-1` exists.
- I2C bus 1 can be scanned.
- SSD1306 responds at `0x3C`.
- `service/tinyoled.service` exists and the installed service is enabled.
- Browser launcher still reports 57 registrations.

The local bridge may be reported as unavailable if it has not been started yet. Optional libraries such as `spidev` or `Adafruit_DHT` are required only for the related peripheral applications.

## 3. Physical OLED check

Run:

```bash
sudo python3 main.py
```

Visually verify:

- splash renders without corruption,
- launcher is readable,
- UP / DOWN / SEL buttons respond,
- at least Clock, System, Settings and one game open and return cleanly,
- no repeated crash/restart loop appears.

This visual step cannot be replaced by CI.

## 4. Optional local bridge

Start the bridge in read-only/control-off mode:

```bash
python3 web-bridge/server.py
```

Then rerun:

```bash
python3 tools/hardware_smoke_test.py
```

`Local bridge health` should report `control=False`.

Only when actively testing actuator paths, opt in explicitly:

```bash
TINY_ALLOW_CONTROL=1 python3 web-bridge/server.py
```

Do not enable control on an untrusted network.

## 5. BRG peripheral sign-off

Test only peripherals actually connected to the intended release hardware. Record `PASS`, `NOT INSTALLED`, or `FAIL` for each:

| Execution path | Hardware / service | Result |
|---|---|---|
| GPIO | Raspberry Pi GPIO | |
| I2C scan | SSD1306 / I2C peripherals | |
| INA219 | Multimeter / power monitor | |
| DHT11/22 | Temperature / humidity | |
| SPI ADC | Plant / oscilloscope-related hardware where applicable | |
| Servo | GPIO18 PWM | |
| Robot car | L298N motor driver | |
| Docker | Local Docker daemon | |
| systemd | Allow-listed services | |
| Pi-hole | Local Pi-hole API | |
| Telegram | Server-side token via environment | |
| E-mail | Server-side IMAP credentials via environment | |

A missing optional peripheral does **not** imply the core TinyOLED desktop failed. The release notes must distinguish core-tested hardware from optional adapters that were not installed.

## 6. Release lock

Only after:

1. CI is green,
2. Pages deployment is green,
3. the core Raspberry Pi / SSD1306 smoke test passes,
4. tested BRG paths are documented,

record the final immutable commit SHA in `RELEASE_READINESS.md` and create the `v1.0.0` tag from that exact SHA.
