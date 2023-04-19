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

    @staticmethod
    def Dispose(target: INode) -> None:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def serach(entry: INode) -> INode:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def show_tree(parent: INode) -> None:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def initialize_tree(parent: INode) -> None:
        raise NotImplementedError