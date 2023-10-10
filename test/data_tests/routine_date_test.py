import os
import sys

sys.path.append(os.path.abspath('.'))

import threading
import unittest
from unittest.mock import MagicMock
from time import sleep
from datetime import datetime, timedelta
from unittest.mock import patch

from src.data.routine_data import RoutineData


class Routine_data_Test(unittest.TestCase):
    def tearDown(self) -> None:
        for thread in threading.enumerate():
            if thread not in (threading.main_thread(),):
                thread.join()
                
        return super().tearDown()
    
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
        
    def test_is_current(self):
        zero = RoutineData()
        self.assertFalse(zero.is_current())
        
        current = RoutineData(minute=1)
        self.assertTrue(current.is_current())
        
    def test_remaine_time(self):
        zero = RoutineData()
        self.assertEqual(zero.remaine(), timedelta())
        
        plus_one = RoutineData(1)
        self.assertGreater(plus_one.remaine(), timedelta())
        
    def test_should_init(self):
        zero = RoutineData()
        self.assertTrue(zero.should_init())
        
        plus_one = RoutineData(minute=1)
        self.assertFalse(plus_one.should_init())
        
        sub_one = RoutineData(minute=-1)
        self.assertTrue(sub_one.should_init)
        
    def test_time_observe(self):
        test_cls = lambda target, wait_time, except_count:\
            type('test', (object,), {
                'target': target,
                'wait_time': wait_time,
                'except_count': except_count})

        test_case = [
            ('one_sec', test_cls(target=RoutineData(minute=1/600), wait_time=0.5, except_count=1)),
            ('zero_sec', test_cls(target=RoutineData(), wait_time=0.1, except_count=0))]
        
        for title, case in test_case:
            with self.subTest(subtest=title, params=case):
                call_mock = MagicMock()
                case.target.on_reach_next(call_mock)
                case.target.time_observe_start()
                sleep(case.wait_time)
                self.assertEqual(call_mock.call_count, case.except_count)
        
if __name__ == '__main__':
    unittest.main()