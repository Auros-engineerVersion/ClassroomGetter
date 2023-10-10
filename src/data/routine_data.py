import threading
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import ClassVar, SupportsInt, Callable

from ..interface import IRoutineData
from ..my_util import public_vars, identity


@dataclass
class RoutineData(IRoutineData):
    @classmethod
    def factory(cls, week, day, hour, minute, pre_time):
        ins = cls(week, day, hour, minute)
        ins.__pre_time = pre_time
        return ins
    
    week: SupportsInt = 0
    day: SupportsInt = 0
    hour: SupportsInt = 0
    minute: SupportsInt = 0
            
    #週、日、時、分の最大の時間
    week_range:  ClassVar[tuple[SupportsInt, SupportsInt]] = (0, 6)
    day_range:   ClassVar[tuple[SupportsInt, SupportsInt]] = (0, 31)
    hour_range:  ClassVar[tuple[SupportsInt, SupportsInt]] = (0, 23)
    minute_range:ClassVar[tuple[SupportsInt, SupportsInt]] = (0, 59)
    
    time_range: ClassVar[list] = [week_range, day_range, hour_range, minute_range]
    
    def __post_init__(self):
        self.__pre_time = datetime.now().replace(microsecond=0)
        self.__thread_stop = False

    def __str__(self) -> str:
        return str(self.next().strftime("%Y-%m-%d %H:%M:%S"))
    
    def __hash__(self) -> int:
        return hash(self.week * self.day * self.hour * self.minute)
    
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, IRoutineData):
            return False
        
        return public_vars(self) == public_vars(o)
    
    def __now(self):
        return datetime.now().replace(microsecond=0)
    
    def reset(self):
        self.week = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        
        self.observe_stop()
        return self
        
    def interval(self) -> timedelta:
        return timedelta(
            weeks=  self.week,
            days=   self.day,
            hours=  self.hour,
            minutes=self.minute
        )
            
    def next(self) -> datetime:
        return self.__pre_time + self.interval()
        
    def remaine(self) -> timedelta:
        if self.is_current():
            remain_time = self.next() - self.__now()
            if remain_time.total_seconds() > 0:
                return remain_time
            else:
                #残り時間が0秒以下であれば
                q = (self.__now() - self.__pre_time) // self.interval()
                self.__pre_time += self.interval() * q
                return timedelta()
        else:
            return timedelta()
    
    def is_current(self) -> bool:
        """
        すべての値が初期値でなければTrueを返す
        """
        #すべての値が初期値でなければ
        x = public_vars(self).values()
        return sum(x) > 0
    
    def should_init(self):
        if self.remaine().total_seconds() <= 0:
            self.__pre_time = datetime.now().replace(microsecond=0)
            return True
        else:
            return False
        
    def time_observe_start(self, when_reach=identity):
        """
        この関数はスレッドが生成される\n
        生成されたスレッドは再帰的に呼び出しを行い、その間隔はself.interval()の10分の1の間隔である\n
        self.intervalの値が0.1よりも小さい場合は0.1秒の間隔で呼び出しを行う
        """
        if not self.is_current() or self.__thread_stop:
            return
        
        if self.should_init():
            when_reach()
        else:
            threading.Timer(
                #最小値は0.1秒。間隔が長すぎるとその分無駄となるため、最大値はintervalの10分の1とする
                interval=max(0.1, self.interval().total_seconds() / 10),
                function=self.time_observe_start,
                args=(when_reach,)
            ).start()
            
    def allow_observe(self):
        self.__thread_stop = False
            
    def observe_stop(self):
        self.__thread_stop = True