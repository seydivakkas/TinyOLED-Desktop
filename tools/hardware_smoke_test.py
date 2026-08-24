#!/usr/bin/env python3
"""TinyOLED Desktop read-only hardware smoke test.

This script intentionally performs no GPIO writes, motor control, WiFi mutation,
service restart, shutdown or reboot. It is safe to run before a release candidate
hardware sign-off.
"""
from __future__ import annotations

import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS: list[dict[str, object]] = []


def record(name: str, ok: bool, detail: str) -> None:
    RESULTS.append({"check": name, "ok": ok, "detail": detail})
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name}: {detail}")


def run(args: list[str], timeout: int = 10) -> tuple[int, str, str]:
    try:
        p = subprocess.run(
            args,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as exc:
        return 999, "", str(exc)


def check_platform() -> None:
    machine = platform.machine()
    system = platform.system()
    model = ""
    model_path = Path("/proc/device-tree/model")
    if model_path.exists():
        try:
            model = model_path.read_text(errors="ignore").replace("\x00", "").strip()
        except Exception:
            pass
    is_linux = system == "Linux"
    is_pi = "Raspberry Pi" in model
    record("Linux platform", is_linux, f"system={system} machine={machine}")
    record("Raspberry Pi model", is_pi, model or "model not detected")


def check_python_syntax() -> None:
    rc, out, err = run([
        sys.executable,
        "-m",
        "compileall",
        "-q",
        "main.py",
        "core",
        "apps",
        "desktop",
        "config",
        "web-bridge/server.py",
    ])
    record("Python syntax", rc == 0, err or out or "compileall clean")


def check_imports() -> None:
    required = ["smbus2"]
    optional = ["RPi.GPIO", "spidev", "Adafruit_DHT"]
    for mod in required:
        ok = importlib.util.find_spec(mod) is not None
        record(f"Required import {mod}", ok, "available" if ok else "missing")
    for mod in optional:
        try:
            ok = importlib.util.find_spec(mod) is not None
        except ModuleNotFoundError:
            ok = False
        record(f"Optional import {mod}", ok, "available" if ok else "not installed; only needed by related apps")


def check_i2c() -> None:
    dev = Path("/dev/i2c-1")
    record("I2C device node", dev.exists(), str(dev))

    tool = shutil.which("i2cdetect")
    if not tool:
        record("i2cdetect", False, "command not found")
        return

    rc, out, err = run([tool, "-y", "1"], timeout=8)
    if rc != 0:
        record("I2C scan", False, err or out or f"exit={rc}")
        return

    normalized = " ".join(out.lower().split())
    oled_found = " 3c " in f" {normalized} " or "3c" in out.lower().split()
    record("I2C scan", True, "bus 1 readable")
    record("SSD1306 @ 0x3C", oled_found, "address detected" if oled_found else "0x3C not present")


def check_service_files() -> None:
    service_src = ROOT / "service" / "tinyoled.service"
    record("systemd service source", service_src.exists(), str(service_src.relative_to(ROOT)) if service_src.exists() else "missing")
    installed = Path("/etc/systemd/system/tinyoled.service")
    record("systemd service installed", installed.exists(), str(installed))

    if shutil.which("systemctl") and installed.exists():
        rc, out, err = run(["systemctl", "is-enabled", "tinyoled.service"], timeout=5)
        record("tinyoled service enabled", rc == 0, out or err or f"exit={rc}")


def check_bridge() -> None:
    url = os.getenv("TINY_BRIDGE_URL", "http://127.0.0.1:8765").rstrip("/") + "/health"
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.loads(response.read())
        ok = bool(data.get("ok"))
        detail = f"control={data.get('control')}"
        record("Local bridge health", ok, detail)
    except Exception as exc:
        record("Local bridge health", False, f"not running or unreachable: {exc}")


def check_catalog() -> None:
    app_modules = [p for p in (ROOT / "apps").glob("*.py") if p.name != "__init__.py"]
    record("Device app module inventory", len(app_modules) >= 50, f"{len(app_modules)} modules discovered")

    shell = (ROOT / "web-simulator/js/shell.js").read_text(encoding="utf-8")
    count = shell.count("this._launcher.register(")
    record("Browser launcher parity", count == 57, f"{count}/57 registrations")


def main() -> int:
    print("TinyOLED Desktop — read-only hardware smoke test")
    print(f"repo={ROOT}")
    check_platform()
    check_python_syntax()
    check_imports()
    check_i2c()
    check_service_files()
    check_bridge()
    check_catalog()

    failures = [r for r in RESULTS if not r["ok"]]
    report = {
        "project": "TinyOLED Desktop",
        "mode": "read-only hardware smoke test",
        "results": RESULTS,
        "failures": len(failures),
    }
    report_path = ROOT / "hardware_smoke_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReport: {report_path}")
    print(f"Summary: {len(RESULTS)-len(failures)}/{len(RESULTS)} checks passed")

    # Optional dependencies and a stopped bridge may be acceptable for a subset
    # of applications, but release sign-off should review every FAIL explicitly.
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
