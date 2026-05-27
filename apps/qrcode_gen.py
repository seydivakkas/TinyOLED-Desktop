"""TinyOLED Desktop — QR Kod Üretici"""
import subprocess
from core.framebuffer import Framebuffer

class QRCodeGenApp:
    NAME="qrcode"; LABEL="QR"; ICON="qr"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.ip="?"; self.matrix=None; self.generate()
    def generate(self):
        try: self.ip=subprocess.check_output(["hostname","-I"],text=True).strip().split()[0]
        except: self.ip="0.0.0.0"
        url=f"http://{self.ip}"
        try:
            import qrcode; qr=qrcode.QRCode(version=1,box_size=1,border=0)
            qr.add_data(url); qr.make(fit=True); self.matrix=qr.get_matrix()
        except:
            # Fallback: basit mock QR
            self.matrix=[[((r+c)%3==0) for c in range(21)] for r in range(21)]
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self.generate()
    def on_long(self): self.on_exit()
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.text("WiFi QR Kod",25,2)
        if self.matrix:
            sz=len(self.matrix); scale=min(2,42//sz)
            sx=(64-sz*scale)//2; sy=12
            for r in range(sz):
                for c in range(sz):
                    if self.matrix[r][c]:
                        fb.rect(sx+c*scale,sy+r*scale,scale,scale,fill=True)
        fb.text(self.ip[:15],65,20)
        fb.text("Telefonla",65,32)
        fb.text("QR tara",65,42)
        fb.text("[SEL] Yenile",2,56)
