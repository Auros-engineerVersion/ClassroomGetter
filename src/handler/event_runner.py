import threading
from typing import Callable


from ..literals import *
from ..interface import *


class EventRunner:
    def __init__(self) -> None:
        self.__events: list[Callable] = []
        
    def add(self, f: Callable):
        self.__events.append(f)
        
    def run_all(self):
        for e in self.__events:
            e()
        
        self.__events.clear()