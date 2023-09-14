import os
import sys
import asyncio

sys.path.append(os.path.abspath('.'))

import tkinter as tk
import unittest
from unittest.mock import patch, MagicMock

from src.gui.custum_widgets import *


class TimeSettersTest(unittest.TestCase):
    def test_is_current_value(self):
        root = tk.Tk()
        setters = TimeSetters(root)
        routine = RoutineData(1,1,1,1)
        setters.set(routine)
        self.assertEqual(setters.values(), routine)
        
class TimerTest(unittest.IsolatedAsyncioTestCase):    
    #@patch('src.gui.custum_widgets.info_boxes.node_box.NodeBox', spec=NodeBox)
    async def test_update_clock(self):
        timer = Timer(tk.Tk(), MagicMock(spec=NodeBox))
        
        #時間が間に合う場合
        call_mock = MagicMock()
        await timer.update_clock(RoutineData(minute=1/60), call_mock, 0.1)
        self.assertEqual(call_mock.call_count, 1)
        
        #間に合わない場合
        call_mock = MagicMock()
        await asyncio.wait_for(timer.update_clock(RoutineData(week=1), call_mock, 0.1), 0.2)
        self.assertLess(call_mock.call_count, 1)