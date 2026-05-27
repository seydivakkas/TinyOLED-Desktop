"""TinyOLED Desktop — Mini Osiloskop (ADC)"""
import time, random
from core.framebuffer import Framebuffer

class OscilloscopeApp:
    NAME="scope"; LABEL="Scope"; ICON="scope"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.samples=[]; self.time_div=1; self.paused=False; self._last=0
    def on_up(self): self.time_div=max(1,self.time_div-1)
    def on_down(self): self.time_div=min(10,self.time_div+1)
    def on_sel(self): self.paused=not self.paused
    def on_long(self): self.on_exit()
    def _read_adc(self):
        # MCP3008 ADC okuma — donanım yoksa simülasyon
        try:
            import spidev
            spi=spidev.SpiDev(); spi.open(0,0); spi.max_speed_hz=1350000
            r=spi.xfer2([1,(8<<4),0]); v=((r[1]&3)<<8)+r[2]; spi.close(); return v
        except: return int(512+400*__import__("math").sin(time.monotonic()*3)+random.randint(-20,20))
    def update(self):
        if self.paused: return
        now=time.monotonic()
        if now-self._last<0.02*self.time_div: return
        self._last=now
        self.samples.append(self._read_adc())
        if len(self.samples)>110: self.samples.pop(0)
    def draw(self, fb: Framebuffer):
        fb.text(f"Scope T:{self.time_div}",2,2)
        fb.text("P" if self.paused else "R",120,2)
        gx,gy,gw,gh=4,12,120,48
        fb.rect(gx-1,gy-1,gw+2,gh+2)
        # Grid çizgileri
        for i in range(1,4):
            y=gy+i*gh//4
            for x in range(gx,gx+gw,4): fb.pixel(x,y)
        for i in range(1,6):
            x=gx+i*gw//6
            for y in range(gy,gy+gh,4): fb.pixel(x,y)
        if len(self.samples)>1:
            for i in range(min(len(self.samples)-1,gw-1)):
                v0=self.samples[-(gw-i)]; v1=self.samples[-(gw-i-1)]
                y0=gy+gh-int(v0*gh/1023); y1=gy+gh-int(v1*gh/1023)
                y0=max(gy,min(gy+gh,y0)); y1=max(gy,min(gy+gh,y1))
                fb.line(gx+i,y0,gx+i+1,y1)
