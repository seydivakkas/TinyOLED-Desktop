"""TinyOLED Desktop — Şifre Üretici"""
import random, string
from core.framebuffer import Framebuffer

class PassGenApp:
    NAME="passgen"; LABEL="Sifre"; ICON="passkey"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.password=""; self.length=16; self.generate()
    def generate(self):
        chars=string.ascii_letters+string.digits+string.punctuation
        self.password="".join(random.SystemRandom().choice(chars) for _ in range(self.length))
    def on_up(self): self.length=min(24,self.length+2); self.generate()
    def on_down(self): self.length=max(8,self.length-2); self.generate()
    def on_sel(self): self.generate()
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("passkey",1,10); fb.text(f"Sifre ({self.length})",12,10)
        fb.hline(0,18,128)
        # İlk satır
        fb.text(self.password[:21],2,24)
        if len(self.password)>21: fb.text(self.password[21:],2,34)
        fb.text("UP/DN:uzunluk",2,48)
        fb.text("SEL:yeni",2,56)
