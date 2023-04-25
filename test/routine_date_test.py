import sys, os
sys.path.append(os.path.abspath('.'))
import unittest
from datetime import datetime, timedelta

from src.data.routine_data import RoutineData

class NormalTest(unittest.TestCase):
    def test_next(self):
        add_time = 5
        routine_data = RoutineData(minute=add_time)
        next = routine_data.next()
        current_time = datetime.now()
        current_time += timedelta(minutes=add_time)
        self.assertEqual(next, current_time)
        
    def test_remaine_time(self):
        zero = RoutineData()
        self.assertEqual(zero.remaine_time(), timedelta())
        
        plus_one = RoutineData(1)
        self.assertGreater(plus_one.remaine_time(), timedelta())
        
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