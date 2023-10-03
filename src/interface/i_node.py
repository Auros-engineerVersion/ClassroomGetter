from __future__ import annotations

from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Callable, Coroutine


class INode(metaclass=ABCMeta):
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
    def next_init_time(self):
        raise NotImplementedError
    
    @abstractproperty
    def edges(self) -> list[INode]:
        raise NotImplementedError
    
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def serach(entry: INode, search_depth: int) -> Coroutine[Callable[[Callable], None]]:
        raise NotImplementedError
    
    @abstractmethod
    def initialize_tree(entry: INode) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def dispose(self) -> None:
        raise NotImplementedError