"""
TinyOLED Desktop — Görev Zamanlayıcı
Periyodik görevleri (saat güncelleme, WiFi kontrol vs.)
ana döngüyü bloke etmeden arka planda çalıştırır.
"""

import threading
import time
from typing import Callable, Dict, Tuple


class Task:
    def __init__(self, name: str, fn: Callable, interval: float):
        self.name     = name
        self.fn       = fn
        self.interval = interval
        self.last_run = 0.0
        self.enabled  = True

    def is_due(self, now: float) -> bool:
        return self.enabled and (now - self.last_run) >= self.interval

    def run(self):
        try:
            self.fn()
        except Exception as e:
            print(f"[SCHED] '{self.name}' hatası: {e}")
        self.last_run = time.monotonic()


class Scheduler:
    """
    Hafif kooperatif zamanlayıcı.
    Ana döngüde her frame `tick()` çağrılır;
    vadesi gelmiş görevler sırayla çalıştırılır.
    """

    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def add(self, name: str, fn: Callable, interval: float):
        """
        Görev ekle.
        interval: saniye cinsinden çalışma aralığı.
        """
        self._tasks[name] = Task(name, fn, interval)

    def remove(self, name: str):
        self._tasks.pop(name, None)

    def enable(self, name: str, state: bool = True):
        if name in self._tasks:
            self._tasks[name].enabled = state

    def tick(self):
        """Her frame çağrılır; vadesi gelen görevleri çalıştırır."""
        now = time.monotonic()
        for task in list(self._tasks.values()):
            if task.is_due(now):
                task.run()

    def run_once(self, name: str):
        """Bir görevi hemen (vadesi gelmeden) tetikle."""
        task = self._tasks.get(name)
        if task:
            task.run()
