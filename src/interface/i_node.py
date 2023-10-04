from __future__ import annotations

from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Callable, Coroutine

from .i_routine_data import IRoutineData
from .i_minimalist_db import IMinimalistID


class ISearchable(metaclass=ABCMeta):
    @abstractmethod
    def search(self, search_depth: int) -> Coroutine[Callable[[Callable], None]]:
        raise NotImplementedError
    
class IDisposable(metaclass=ABCMeta):
    @abstractmethod
    def dispose(self) -> None:
        raise NotImplementedError
    
class IHasEdges(metaclass=ABCMeta):
    @abstractproperty
    def parent(self) -> IMinimalistID:
        raise NotImplementedError
    
    @abstractproperty
    def edges(self) -> list[IMinimalistID]:
        raise NotImplementedError
    
    @abstractproperty
    def raw_edges(self) -> list[IHasEdges]:
        raise NotImplementedError

class INodeProperty(metaclass=ABCMeta):
    @abstractproperty
    def id(self):
        raise NotImplementedError
    
    @abstractproperty
    def key(self):
        raise NotImplementedError
    
    @abstractproperty
    def url(self):
        raise NotImplementedError
        
    @abstractproperty
    def tree_height(self):
        raise NotImplementedError
    
    @abstractproperty
    def next_init_time(self) -> IRoutineData:
        raise NotImplementedError

    @abstractproperty
    def include_this_to_path(self) -> bool:
        raise NotImplementedError