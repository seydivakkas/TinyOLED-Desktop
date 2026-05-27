"""TinyOLED Desktop — SD Kart MP3 Çalar"""
import subprocess, os, time
from pathlib import Path
from core.framebuffer import Framebuffer
from core.font import Font

MUSIC_DIR=Path("/home/pi/Music")

class MP3PlayerApp:
    NAME="mp3"; LABEL="Muzik"; ICON="music"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self._cursor=0; self._scroll=0
        self.tracks=[]; self.playing=False; self.current=""; self._proc=None
        self._scan()
    def _scan(self):
        self.tracks=[]
        try:
            for f in sorted(MUSIC_DIR.glob("**/*.mp3")):
                self.tracks.append({"name":f.stem[:20],"path":str(f)})
        except: pass
        if not self.tracks:
            self.tracks=[{"name":"(bos - MP3 ekleyin)","path":""}]
    def on_up(self):
        if self._cursor>0: self._cursor-=1
        if self._cursor<self._scroll: self._scroll=self._cursor
    def on_down(self):
        if self._cursor<len(self.tracks)-1: self._cursor+=1
        if self._cursor>=self._scroll+4: self._scroll+=1
    def on_sel(self):
        t=self.tracks[self._cursor]
        if not t["path"]: return
        if self.playing: self._stop()
        else: self._play(t)
    def on_long(self): self._stop(); self.on_exit()
    def _play(self, track):
        self._stop()
        try:
            self._proc=subprocess.Popen(["mpv","--no-video","--really-quiet",track["path"]],
                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            self.playing=True; self.current=track["name"]
        except: self.playing=False
    def _stop(self):
        if self._proc:
            try: self._proc.terminate()
            except: pass
            self._proc=None
        self.playing=False; self.current=""
    def update(self):
        if self._proc and self._proc.poll() is not None:
            self.playing=False; self.current=""
            if self._cursor<len(self.tracks)-1:
                self._cursor+=1; self._play(self.tracks[self._cursor])
    def draw(self, fb: Framebuffer):
        fb.icon("music",1,10)
        if self.playing: fb.text(f">{self.current[:16]}",12,10)
        else: fb.text("MP3 Calar",12,10)
        fb.hline(0,18,128); y=20
        vis=self.tracks[self._scroll:self._scroll+4]
        for i,t in enumerate(vis):
            ai=self._scroll+i; sel=(ai==self._cursor)
            if sel: fb.rect(0,y-1,128,9,fill=True)
            mark=">" if self.playing and t["name"]==self.current else " "
            fb.text(f"{mark}{t['name'][:20]}",1,y,on=not sel); y+=9
        if self.playing: fb.text("SEL:durdur",2,56)
        else: fb.text("SEL:oynat",2,56)
        fb.text("LONG:cikis",75,56)
