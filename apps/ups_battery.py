"""TinyOLED Desktop — UPS Pil Durumu"""
import time
from core.framebuffer import Framebuffer

class UPSBatteryApp:
    NAME="ups"; LABEL="UPS"; ICON="ups"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.voltage=4.15; self.pct=85; self.charging=True; self._last=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self._read()
    def on_long(self): self.on_exit()
    def _read(self):
        try:
            import smbus2; bus=smbus2.SMBus(1)
            raw=bus.read_word_data(0x36,0x02); self.voltage=((raw>>8)|(raw<<8)&0xFFFF)*0.00125
            raw=bus.read_word_data(0x36,0x04); self.pct=min(100,((raw>>8)|(raw<<8)&0xFFFF)//256)
            bus.close()
        except: pass
    def update(self):
        now=time.monotonic()
        if now-self._last<5: return
        self._last=now; self._read()
    def draw(self, fb: Framebuffer):
        fb.icon("ups",1,10); fb.text("UPS Pil Durumu",12,10); fb.hline(0,18,128)
        # Büyük pil görseli
        fb.rect(20,24,88,20); fb.rect(108,30,4,8,fill=True)
        fill_w=int(84*self.pct/100)
        if fill_w>0: fb.rect(22,26,fill_w,16,fill=True)
        fb.text_centered(f"%{self.pct}",34)
        fb.text(f"Voltaj: {self.voltage:.2f}V",10,50)
        fb.text("Sarj" if self.charging else "Pil",90,50)
