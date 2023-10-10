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
    def on_reach_next(self, f, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def time_observe_start(self):
        raise NotImplementedError