from __future__ import annotations
from abc import ABCMeta, abstractmethod

class INode(metaclass=ABCMeta):
    @abstractmethod
    def edges(self, add_value: INode = None) -> set[INode]:
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
    def serach(entry: INode) -> INode:
        raise NotImplementedError
    
    @abstractmethod
    def dispose(self) -> None:
        raise NotImplementedError