from __future__ import annotations
from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Coroutine, Callable

class IBrowserControlData(metaclass=ABCMeta):
    def __init__(self) -> None:
        raise NotImplementedError
    
    def __del__(self):
        raise NotImplementedError