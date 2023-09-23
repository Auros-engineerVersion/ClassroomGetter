from abc import ABCMeta, abstractmethod

class InputBase(metaclass=ABCMeta):
    @abstractmethod
    def set(self, value) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get(self):
        raise NotImplementedError