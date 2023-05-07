from dataclasses import dataclass
from typing import SupportsInt
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

@dataclass
class RoutineData:
    week: SupportsInt = 0
    day: SupportsInt = 0
    hour: SupportsInt = 0
    minute: SupportsInt = 0
    
    def __post_init__(self):
        self.__pre_time = datetime.now().replace(microsecond=0)

    def __str__(self) -> str:
        return str(self.next().strftime("%Y-%m-%d %H:%M:%S"))
    
    def __now(self):
        return datetime.now().replace(microsecond=0)
    
    def interval(self) -> timedelta:
        return timedelta(
            weeks=self.week,
            days=self.day,
            hours=self.hour,
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
                q = (self.__now() - self.__pre_time) // self.interval()
                self.__pre_time += self.interval() * q
                return timedelta()
        else:
            return timedelta()
    
    def is_current(self) -> bool:
        #すべての値が初期値でなければ
        return self.week + self.day + self.hour + self.minute > 0
    
    def should_init(self):
        if self.remaine().total_seconds() <= 0:
            self.__pre_time = datetime.now().replace(microsecond=0)
            return True
        else:
            return False