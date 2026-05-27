"""TinyOLED Desktop — Servo Motor Kontrol Paneli"""
import math
from core.framebuffer import Framebuffer

class ServoApp:
    NAME="servo"; LABEL="Servo"; ICON="servo"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.angle=90; self._active=False
    def on_up(self): self.angle=min(180,self.angle+5)
    def on_down(self): self.angle=max(0,self.angle-5)
    def on_sel(self):
        self._active=True
        try:
            import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(18,GPIO.OUT)
            pwm=GPIO.PWM(18,50); pwm.start(0)
            duty=self.angle/18+2; pwm.ChangeDutyCycle(duty)
            import time; time.sleep(0.5); pwm.stop(); GPIO.cleanup()
        except: pass
        self._active=False
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("servo",1,10); fb.text("Servo Motor",12,10); fb.hline(0,18,128)
        # Yarım daire kadran
        cx,cy,r=64,50,28
        for deg in range(0,181,5):
            rad=math.radians(180-deg)
            fb.pixel(int(cx+r*math.cos(rad)),int(cy-r*math.sin(rad)))
        # İbre
        rad=math.radians(180-self.angle)
        nx=int(cx+(r-5)*math.cos(rad)); ny=int(cy-(r-5)*math.sin(rad))
        fb.line(cx,cy,nx,ny); fb.circle(cx,cy,2,fill=True)
        fb.text(f"{self.angle}",cx-8,22); fb.text("SEL:tetikle",2,56)
