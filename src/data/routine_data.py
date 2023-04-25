from dataclasses import dataclass
from typing import SupportsInt
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

@dataclass
class RoutineData:
    year: SupportsInt = 0
    month: SupportsInt = 0
    week: SupportsInt = 0
    day: SupportsInt = 0
    hour: SupportsInt = 0
    minute: SupportsInt = 0
    
    def __post_init__(self):
        self.__pre_time = datetime.now().replace(microsecond=0)
        
    def __str__(self) -> str:
        return str(self.next().strftime("%Y-%m-%d %H:%M:%S"))
            
    def next(self) -> datetime:
        return self.__pre_time + relativedelta(
            years=self.year, 
            months=self.month,
            weeks=self.week,
            days=self.day,
            hours=self.hour,
            minutes=self.minute
        )
        
    def remaine_time(self):
        if self.is_current():
            return self.next() - datetime.now().replace(microsecond=0)
        else:
            return timedelta()
    
    def is_current(self) -> bool:
        #すべての値が初期値でなければ
        return self.year + self.month + self.week + self.day + self.hour + self.minute > 0
    
    def should_init(self):
        if self.remaine_time().total_seconds() > 0:
            return False
        else:
            self.__pre_time = datetime.now().replace(microsecond=0)
            return True