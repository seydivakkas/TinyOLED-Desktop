"""TinyOLED Desktop — İnternet Radyo Çalar"""
import subprocess
from core.framebuffer import Framebuffer
STATIONS=[
    {"name":"TRT FM","url":"https://trturk.listenpluscdn.com/trturk/playlist.m3u8"},
    {"name":"LoFi HipHop","url":"https://streams.ilovemusic.de/iloveradio17.mp3"},
    {"name":"Jazz FM","url":"https://edge-bauerm-03-gos2.sharp-stream.com/jazzfm.mp3"},
    {"name":"Classical","url":"https://live.musopen.org:8085/streamvbr0"},
]

class RadioApp:
    NAME="radio"; LABEL="Radyo"; ICON="radio"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._cursor=0; self.playing=False; self._proc=None
    def on_up(self): self._cursor=max(0,self._cursor-1)
    def on_down(self): self._cursor=min(len(STATIONS)-1,self._cursor+1)
    def on_sel(self):
        if self.playing: self._stop()
        else: self._play()
    def on_long(self): self._stop(); self.on_exit()
    def _play(self):
        self._stop()
        try:
            self._proc=subprocess.Popen(["mpv","--no-video","--really-quiet",STATIONS[self._cursor]["url"]],
                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            self.playing=True
        except: pass
    def _stop(self):
        if self._proc:
            try: self._proc.terminate()
            except: pass; self._proc=None
        self.playing=False
    def update(self): pass
    def draw(self, fb: Framebuffer):
        fb.icon("radio",1,10); fb.text("Internet Radyo",12,10); fb.hline(0,18,128); y=22
        for i,s in enumerate(STATIONS):
            sel=(i==self._cursor)
            if sel: fb.rect(0,y-1,128,10,fill=True)
            mark=">" if self.playing and i==self._cursor else " "
            fb.text(f"{mark}{s['name']}",2,y,on=not sel); y+=11
        fb.text("SEL:oynat/dur" if not self.playing else "SEL:durdur",2,56)
