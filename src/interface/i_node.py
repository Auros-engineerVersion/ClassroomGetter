from __future__ import annotations
from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Coroutine, Callable

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
    def edges(self) -> set[INode]:
        raise NotImplementedError
    
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, other) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other) -> bool:
        raise NotImplementedError

    @abstractmethod
    def serach(entry: INode) -> Coroutine[Callable[[Callable], None]]:
        raise NotImplementedError
    
    @abstractmethod
    def initialize_tree(entry: INode) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def dispose(self) -> None:
        raise NotImplementedError