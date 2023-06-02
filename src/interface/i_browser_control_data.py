from __future__ import annotations
from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Coroutine, Callable

class IBrowserControlData(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, setting, driver = None, wait = None) -> None:
        pass
        
    @abstractproperty
    def driver(self):
        raise NotImplementedError
    
    @abstractproperty
    def wait(self):
        raise NotImplementedError