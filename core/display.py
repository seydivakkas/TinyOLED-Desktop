"""
TinyOLED Desktop — SSD1306 I2C Display Driver
Raspberry Pi Zero W + 0.96" SSD1306 128x64 OLED

I2C Pinout:
  SDA → GPIO 2  (Pin 3)
  SCL → GPIO 3  (Pin 5)
  VCC → 3.3V
  GND → GND
"""

import time
import smbus2 as smbus


# ── SSD1306 Command Bytes ──────────────────────────────────────
SSD1306_DISPLAY_OFF          = 0xAE
SSD1306_DISPLAY_ON           = 0xAF
SSD1306_SET_CONTRAST         = 0x81
SSD1306_ENTIRE_DISPLAY_ON    = 0xA5
SSD1306_RESUME_TO_RAM        = 0xA4
SSD1306_NORMAL_DISPLAY       = 0xA6
SSD1306_INVERT_DISPLAY       = 0xA7
SSD1306_SET_MULTIPLEX        = 0xA8
SSD1306_SET_DISPLAY_OFFSET   = 0xD3
SSD1306_SET_START_LINE       = 0x40
SSD1306_MEMORY_MODE          = 0x20
SSD1306_SET_COLUMN_ADDR      = 0x21
SSD1306_SET_PAGE_ADDR        = 0x22
SSD1306_COM_SCAN_INC         = 0xC0
SSD1306_COM_SCAN_DEC         = 0xC8
SSD1306_SET_COM_PINS         = 0xDA
SSD1306_SET_CLOCK_DIV        = 0xD5
SSD1306_SET_PRECHARGE        = 0xD9
SSD1306_SET_VCOM_DETECT      = 0xDB
SSD1306_CHARGE_PUMP          = 0x8D

DISPLAY_WIDTH  = 128
DISPLAY_HEIGHT = 64
I2C_ADDR       = 0x3C
I2C_BUS        = 1


class SSD1306:
    """
    Low-level SSD1306 OLED display controller via I2C.
    Manages a 128×64 1-bit framebuffer.
    """

    def __init__(self, bus: int = I2C_BUS, address: int = I2C_ADDR):
        self.bus     = smbus.SMBus(bus)
        self.address = address
        self.width   = DISPLAY_WIDTH
        self.height  = DISPLAY_HEIGHT
        self.pages   = self.height // 8             # 8 pages
        self._buffer = bytearray(self.width * self.pages)

        self._initialize()

    # ── Private ────────────────────────────────────────────────
    def _cmd(self, *commands):
        """Write one or more commands to SSD1306."""
        for cmd in commands:
            self.bus.write_byte_data(self.address, 0x00, cmd)

    def _initialize(self):
        """Full SSD1306 initialization sequence."""
        self._cmd(
            SSD1306_DISPLAY_OFF,
            SSD1306_SET_CLOCK_DIV,   0x80,
            SSD1306_SET_MULTIPLEX,   0x3F,   # 1/64 duty
            SSD1306_SET_DISPLAY_OFFSET, 0x00,
            SSD1306_SET_START_LINE,
            SSD1306_CHARGE_PUMP,     0x14,   # internal VCC
            SSD1306_MEMORY_MODE,     0x00,   # horizontal addressing
            0xA1,                            # segment remap
            SSD1306_COM_SCAN_DEC,
            SSD1306_SET_COM_PINS,    0x12,
            SSD1306_SET_CONTRAST,    0xCF,
            SSD1306_SET_PRECHARGE,   0xF1,
            SSD1306_SET_VCOM_DETECT, 0x40,
            SSD1306_RESUME_TO_RAM,
            SSD1306_NORMAL_DISPLAY,
            SSD1306_DISPLAY_ON,
        )
        self.clear()
        self.show()

    # ── Public ──────────────────────────────────────────────────
    def clear(self):
        """Fill buffer with zeros (all pixels off)."""
        for i in range(len(self._buffer)):
            self._buffer[i] = 0

    def fill(self):
        """Fill buffer with ones (all pixels on)."""
        for i in range(len(self._buffer)):
            self._buffer[i] = 0xFF

    def pixel(self, x: int, y: int, on: bool = True):
        """Set single pixel (x, y). Origin = top-left."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        page   = y // 8
        bit    = y % 8
        index  = page * self.width + x
        if on:
            self._buffer[index] |= (1 << bit)
        else:
            self._buffer[index] &= ~(1 << bit)

    def get_pixel(self, x: int, y: int) -> bool:
        """Read single pixel value."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        page  = y // 8
        bit   = y % 8
        index = page * self.width + x
        return bool(self._buffer[index] & (1 << bit))

    def blit(self, buf: bytearray):
        """Blit an external buffer directly into the display buffer."""
        length = min(len(buf), len(self._buffer))
        self._buffer[:length] = buf[:length]

    def invert(self, enable: bool):
        """Toggle inverted display mode."""
        self._cmd(SSD1306_INVERT_DISPLAY if enable else SSD1306_NORMAL_DISPLAY)

    def brightness(self, level: int):
        """Set contrast/brightness 0–255."""
        self._cmd(SSD1306_SET_CONTRAST, max(0, min(255, level)))

    def power(self, on: bool):
        """Turn display panel on or off."""
        self._cmd(SSD1306_DISPLAY_ON if on else SSD1306_DISPLAY_OFF)

    def show(self):
        """Flush internal buffer to OLED hardware via I2C."""
        self._cmd(
            SSD1306_SET_COLUMN_ADDR, 0, self.width - 1,
            SSD1306_SET_PAGE_ADDR,   0, self.pages - 1,
        )
        chunk_size = 32
        data_len   = len(self._buffer)
        offset     = 0
        while offset < data_len:
            chunk = list(self._buffer[offset: offset + chunk_size])
            self.bus.write_i2c_block_data(self.address, 0x40, chunk)
            offset += chunk_size

    def get_buffer(self) -> bytearray:
        """Return a copy of the current framebuffer."""
        return bytearray(self._buffer)

    def set_buffer(self, buf: bytearray):
        """Replace internal buffer with provided bytes."""
        self.blit(buf)

    def close(self):
        """Release I2C bus."""
        self.power(False)
        self.bus.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
