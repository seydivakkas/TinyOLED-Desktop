# Known Limitations

TinyOLED Desktop is designed for a constrained Raspberry Pi + SSD1306 environment. The browser simulator improves inspectability, but it does not replace hardware validation.

## Hardware-dependent behavior

- Physical GPIO button handling requires a Raspberry Pi or a compatible GPIO environment.
- SSD1306 I2C rendering requires the physical display and a correctly configured I2C bus.
- Optional applications that use DHT sensors, INA219, MCP3008, HMC5883L, servo motors, motor drivers or other peripherals require the corresponding hardware.
- Hardware addresses, wiring and electrical conditions can differ between installations and must be verified locally.

## Browser simulator scope

- The simulator reproduces the desktop interaction model and visual behavior, not the electrical behavior of GPIO/I2C peripherals.
- Hardware sensor values, system services, privileged commands and device-specific integrations may be mocked, unavailable or represented only at UI level.
- Simulator parity should therefore be interpreted as interface/interaction evidence rather than proof of hardware correctness.

## Environment and privileges

- Some system-management applications require Linux utilities or elevated privileges.
- Network-dependent applications require external connectivity and may depend on third-party service availability.
- Optional applications may require additional packages beyond the minimal core installation.

## Release policy

A `v1.0.0` release should only be published after the release commit passes CI and a Raspberry Pi + SSD1306 smoke test. Hardware-specific claims must remain scoped to the tested configuration.
