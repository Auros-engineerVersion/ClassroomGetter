import os
import sys

sys.path.append(os.path.abspath('.'))

import threading
import unittest
from unittest.mock import MagicMock
from time import sleep
from datetime import datetime, timedelta
from unittest.mock import patch

from src.my_util import identity
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
        
    def test_is_current(self):
        zero = RoutineData()
        self.assertFalse(zero.is_current())
        
        current = RoutineData(minute=1)
        self.assertTrue(current.is_current())
        
    def test_remaine_time(self):
        zero = RoutineData()
        self.assertEqual(zero.remaine(), timedelta())
        
        plus_one = RoutineData(minute=1)
        self.assertEqual(plus_one.remaine(), timedelta(minutes=1))
        
    def test_should_init(self):
        zero = RoutineData()
        self.assertTrue(zero.should_init())
        
        plus_one = RoutineData(minute=1/60)
        self.assertFalse(plus_one.should_init())
        sleep(1)
        self.assertTrue(plus_one.should_init())
        
        sub_one = RoutineData(minute=-1)
        self.assertTrue(sub_one.should_init)
        
    def test_time_observe_start_can_stop(self):
        timeout_mock = MagicMock()
        timeout_mock.side_effect = [*range(3), TimeoutError]
        
        not_raise = RoutineData()
        not_raise.time_observe_start(timeout_mock)
        
        thread_stop = RoutineData(1/60)
        thread_stop.reject_observe()
        thread_stop.time_observe_start((call_mock := MagicMock()))
        self.assertEqual(call_mock.call_count, 0)
        
    def test_time_observe_start(self):
        test_cls = lambda target, wait_time=1, except_count=0, scrambler=identity:\
            type('test', (object,), {
                'target': target,
                'wait_time': wait_time,
                'except_count': except_count,
                'scrambler': scrambler})

        test_case = [
            ('one_sec', test_cls(
                target=RoutineData(minute=1/60),
                wait_time=1,
                except_count=1)),
            
            ('zero_sec', test_cls(
                target=RoutineData(),
                except_count=0)),
        ]
        
        for title, case in test_case:
            with self.subTest(subtest=title, params=case):
                try:
                    call_mock = MagicMock()
                    case.target.time_observe_start(call_mock)
                    sleep(case.wait_time)
                    case.scrambler()
                    self.assertEqual(call_mock.call_count, case.except_count)
                finally:
                    case.target.reject_observe()
                                        
if __name__ == '__main__':
    unittest.main()