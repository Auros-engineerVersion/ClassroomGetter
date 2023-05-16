from dataclasses import dataclass
from typing import SupportsInt, ClassVar
from datetime import datetime, timedelta

@dataclass
class RoutineData:
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