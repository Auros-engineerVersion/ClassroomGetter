import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
import tkinter as tk

from src.data.routine_data import RoutineData
from src.gui.custum_widgets.infomations import *

class TimeSettersTest(unittest.TestCase):
    def test_is_current_value(self):
        root = tk.Tk()
        setters = TimeSetters(root)
        routine = RoutineData(1,1,1,1)
        setters.set(routine)
        self.assertEqual(setters.values(), routine)