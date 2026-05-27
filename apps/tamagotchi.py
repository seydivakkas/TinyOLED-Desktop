"""
TinyOLED Desktop — Tamagotchi Sanal Evcil Hayvan
UP/DOWN: Menü, SEL: Aksiyon, LONG: Çıkış
"""
import time, json
from pathlib import Path
from core.framebuffer import Framebuffer

SAVE = Path("/home/pi/tiny-oled-desktop/config/pet_state.json")
ACTIONS = ["Besle", "Oyna", "Uyut", "Temizle"]

class TamagotchiApp:
    NAME = "tamagotchi"; LABEL = "Pet"; ICON = "pet"

    def __init__(self, on_exit):
        self.on_exit = on_exit; self._cursor = 0; self._tick = 0
        self.hunger = 70; self.happy = 70; self.energy = 70; self.clean = 70
        self._load()

    def _load(self):
        try:
            d = json.loads(SAVE.read_text())
            self.hunger = d.get("hunger", 70); self.happy = d.get("happy", 70)
            self.energy = d.get("energy", 70); self.clean = d.get("clean", 70)
        except: pass

    def _save(self):
        try: SAVE.write_text(json.dumps({"hunger":self.hunger,"happy":self.happy,"energy":self.energy,"clean":self.clean}))
        except: pass

    def on_up(self): self._cursor = (self._cursor - 1) % len(ACTIONS)
    def on_down(self): self._cursor = (self._cursor + 1) % len(ACTIONS)
    def on_sel(self):
        a = ACTIONS[self._cursor]
        if a == "Besle": self.hunger = min(100, self.hunger + 20)
        elif a == "Oyna": self.happy = min(100, self.happy + 20); self.energy = max(0, self.energy - 10)
        elif a == "Uyut": self.energy = min(100, self.energy + 30)
        elif a == "Temizle": self.clean = min(100, self.clean + 25)
        self._save()
    def on_long(self): self._save(); self.on_exit()

    def update(self):
        self._tick += 1
        if self._tick % 60 == 0:
            self.hunger = max(0, self.hunger - 2); self.happy = max(0, self.happy - 1)
            self.energy = max(0, self.energy - 1); self.clean = max(0, self.clean - 1)

    def draw(self, fb: Framebuffer):
        # Pet yüzü
        cx, cy = 40, 32
        fb.circle(cx, cy, 14)
        eye_off = 3 if self._tick % 40 < 35 else 0
        fb.rect(cx-6, cy-4, 3, 3+eye_off, fill=True)
        fb.rect(cx+4, cy-4, 3, 3+eye_off, fill=True)
        mood = (self.hunger + self.happy + self.energy + self.clean) / 4
        if mood > 50:
            fb.line(cx-4, cy+4, cx, cy+7); fb.line(cx, cy+7, cx+4, cy+4)
        else:
            fb.line(cx-4, cy+7, cx, cy+4); fb.line(cx, cy+4, cx+4, cy+7)
        # Barlar
        fb.text("Tok", 68, 12); fb.progress_bar(88, 12, 38, 6, self.hunger)
        fb.text("Mut", 68, 22); fb.progress_bar(88, 22, 38, 6, self.happy)
        fb.text("Enj", 68, 32); fb.progress_bar(88, 32, 38, 6, self.energy)
        fb.text("Tem", 68, 42); fb.progress_bar(88, 42, 38, 6, self.clean)
        # Menü
        for i, a in enumerate(ACTIONS):
            x = i * 32; sel = (i == self._cursor)
            if sel: fb.rect(x, 54, 31, 9, fill=True)
            fb.text(a[:4], x+2, 55, on=not sel)
