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
        
    def test_should_init(self):
        routine_data = RoutineData()
        self.assertFalse(routine_data.should_init())
        
        routine_data = RoutineData(minute=1)
        self.assertFalse(routine_data.should_init())
        
        routine_data = RoutineData(minute=-1)
        self.assertTrue(routine_data.should_init)