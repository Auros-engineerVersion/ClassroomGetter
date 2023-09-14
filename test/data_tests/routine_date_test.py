import os
import sys

sys.path.append(os.path.abspath('.'))
import time
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.data.routine_data import RoutineData


class Routine_data_Test(unittest.TestCase):
    def test_reset(self):
        data = RoutineData(0,0,0,1)
        self.assertEqual(data.reset(), RoutineData())
    
    def test_next(self):
        add_time = 5
        routine_data = RoutineData(minute=add_time)
        next = routine_data.next()
        current_time = datetime.now().replace(microsecond=0)
        current_time += timedelta(minutes=add_time)
        self.assertEqual(next, current_time)
        
    def test_remaine_time(self):
        zero = RoutineData()
        self.assertEqual(zero.remaine(), timedelta())
        
        plus_one = RoutineData(1)
        self.assertGreater(plus_one.remaine(), timedelta())
        
    def test_is_current(self):
        zero = RoutineData()
        self.assertFalse(zero.is_current())
        
        current = RoutineData(minute=1)
        self.assertTrue(current.is_current())
        
    def test_should_init(self):
        zero = RoutineData()
        self.assertTrue(zero.should_init())
        
        plus_one = RoutineData(minute=1)
        self.assertFalse(plus_one.should_init())
        
        sub_one = RoutineData(minute=-1)
        self.assertTrue(sub_one.should_init)
        
if __name__ == '__main__':
    unittest.main()