"""TinyOLED Desktop — IP Kamera Önizleyici"""
from core.framebuffer import Framebuffer

class IPCamApp:
    NAME="ipcam"; LABEL="Kamera"; ICON="camera"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.frame_data=None; self.url="http://192.168.1.100/capture"
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): self._capture()
    def on_long(self): self.on_exit()
    def _capture(self):
        try:
            import urllib.request
            from io import BytesIO
            r=urllib.request.urlopen(self.url,timeout=5); data=r.read()
            # JPEG → 1-bit dithering (basitleştirilmiş)
            self.frame_data=data  # Gerçekte PIL ile işlenir
        except: pass
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("camera",1,10); fb.text("IP Kamera",12,10); fb.hline(0,18,128)
        if self.frame_data:
            fb.text_centered("Goruntu alindi",35)
        else:
            fb.text_centered("Kamera yok",30)
            fb.text_centered("SEL ile yakala",42)
        fb.text(self.url[:20],2,56)
