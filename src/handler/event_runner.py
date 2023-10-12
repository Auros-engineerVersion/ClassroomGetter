import threading
from typing import Callable


from ..literals import *
from ..interface import *


class EventRunner:
    def __init__(self) -> None:
        self.__current_thread: threading.Thread = None
        self.__events: list[Callable] = []
        
    def add(self, f: Callable):
        self.__events.append(f)
        
    def run_all(self):
        def _run():
            for e in self.__events:
                e()
        
            self.__events.clear()
        
        if self.__current_thread is None or not self.__current_thread.is_alive():
            self.__current_thread = threading.Thread(target=_run)
            self.__current_thread.start()