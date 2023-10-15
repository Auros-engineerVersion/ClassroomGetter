from __future__ import annotations

from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Callable, Coroutine

class IMinimalistID(metaclass=ABCMeta):
    @abstractmethod
    def value(self, db):
        raise NotImplementedError
    
class IMinimalistRecode(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other):
        raise NotImplementedError
    
    @abstractmethod
    def __eq__(self, __value: IMinimalistRecode) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError
    
class IMinimalistDB(metaclass=ABCMeta):
    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError
        
    @abstractmethod
    def add(self, recode: IMinimalistRecode) -> IMinimalistID:
        raise NotImplementedError
    
    @abstractmethod
    def get_fromID(self, id) -> IMinimalistRecode:
        raise NotImplementedError