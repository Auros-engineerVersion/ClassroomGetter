import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch
import tkinter as tk

from src.gui.custum_widgets import *

class TimeSettersTest(unittest.TestCase):
    def test_is_current_value(self):
        root = tk.Tk()
        setters = TimeSetters(root)
        routine = RoutineData(1,1,1,1)
        setters.set(routine)
        self.assertEqual(setters.values(), routine)
        
class TimerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tk.Tk()
        
    @patch('...src.gui.custum_widgets.info_boxes.node_box.NodeBox', spec=NodeBox)
    def test_update_clock(self, m_node_box):
        timer = Timer(self.root, m_node_box)