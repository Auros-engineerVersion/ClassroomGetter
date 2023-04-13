from __future__ import annotations
from abc import ABCMeta, abstractmethod

class INode(metaclass=ABCMeta):
    @abstractmethod
    def edges(self, add_value: INode = None) -> list[INode]:
        raise NotImplementedError
    
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @staticmethod
    def Dispose(target: INode) -> None:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def ShowTree(parent: INode) -> None:
        raise NotImplementedError