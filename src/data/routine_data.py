from dataclasses import dataclass
import dataclasses
from datetime import datetime

@dataclass
class RoutineData:
    interval_time: datetime = datetime(
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
    
    pre_time: datetime
    
    def next_time(self):
        
    
    def year(self, value = None):
        if value != None and value != 0:
            self.interval_time.year = value
        
        return self.interval_time.year
            
    def month(self, value = None):
        if value != None and 0 < value < 13:
            self.interval_time.month = value
        
        return self.interval_time.month
    
    def day(self, value = None):
        if value != None and 0 < value < 32:
            self.interval_time.day = value
            
        return self.interval_time.day
    
    def hour(self, value = None):
        if value != None and 0 < value < 25:
            self.interval_time.hour = value
            
        return self.interval_time.hour
    
    def minute(self, value = None):
        if value != None and 0 < 60:
            self.interval_time.minute = value
            
        return self.interval_time.minute
        
    def delta(self):
        return datetime.now() - self.interval_time