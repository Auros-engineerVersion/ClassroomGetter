from abc import ABCMeta, abstractmethod


class IRoutineData(metaclass=ABCMeta):
    @abstractmethod
    def reset(self):
        raise NotImplementedError
    
    @abstractmethod
    def interval(self):
        raise NotImplementedError
    
    @abstractmethod
    def next(self):
        raise NotImplementedError
    
    @abstractmethod
    def remaine(self):
        raise NotImplementedError
    
    @abstractmethod
    def is_current(self):
        raise NotImplementedError
    
    @abstractmethod
    def time_observe_start(self, when_reach):
        raise NotImplementedError