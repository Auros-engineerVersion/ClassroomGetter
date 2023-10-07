import asyncio
import os
import sys

sys.path.append(os.path.abspath('.'))

import tkinter as tk
import unittest
from unittest.mock import MagicMock, patch

from src.gui.custum_widgets import *


class TimeSettersTest(unittest.TestCase):
    def test_is_current_value(self):
        setters = TimeSetters(tk.Tk())
        routine = RoutineData(1,1,1,1)
        setters.set(routine)
        self.assertEqual(setters.value(), routine)
        
class TimerTest(unittest.TestCase):    
    #@patch('src.gui.custum_widgets.info_boxes.node_box.NodeBox', spec=NodeBox)
    def test_update_clock(self):
        timer = Timer(tk.Tk(), MagicMock(spec=NodeBox))
        
        call_mock = MagicMock()
        
        timer.clock_event_publish(
            dead_line=RoutineData(minute=0.1/60), interval_ms=10)
        self.assertEqual(call_mock.call_count, 0)