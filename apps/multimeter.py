"""TinyOLED Desktop — Dijital Multimetre (INA219)"""
import time
from core.framebuffer import Framebuffer

class MultimeterApp:
    NAME="multimeter"; LABEL="Volt"; ICON="volt"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.voltage=0.0; self.current=0.0; self.power=0.0; self._last=0
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self.update()
    def on_long(self): self.on_exit()
    def _read_ina219(self):
        try:
            import smbus2; bus=smbus2.SMBus(1); addr=0x40
            raw=bus.read_word_data(addr,0x02); self.voltage=((raw>>8)|(raw<<8)&0xFFFF)*0.001
            raw=bus.read_word_data(addr,0x04); self.current=((raw>>8)|(raw<<8)&0xFFFF)*0.1
            self.power=self.voltage*self.current/1000; bus.close()
        except: self.voltage=5.02; self.current=120.5; self.power=0.604
    def update(self):
        now=time.monotonic()
        if now-self._last<1.0: return
        self._last=now; self._read_ina219()
    def draw(self, fb: Framebuffer):
        fb.icon("volt",1,10); fb.text("Multimetre",12,10); fb.hline(0,18,128)
        # Büyük voltaj gösterimi
        v_str=f"{self.voltage:.2f}V"
        fb.text(v_str,10,24)
        fb.progress_bar(10,34,108,6,self.voltage,max_val=12.0)
        fb.text(f"Akim: {self.current:.1f}mA",10,44)
        fb.text(f"Guc : {self.power:.3f}W",10,54)
