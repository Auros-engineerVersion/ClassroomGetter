import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import MagicMock, patch

from src.gui.custum_widgets import *


class SettingGroupTest(unittest.TestCase):
    def test_boxes(self):
        values = {'a': {'value': '1', 'description': 'a'}, 'b': {'value': '2', 'description': 'b'}}
        sg = SettingGroup(tk.Tk(), 'hoge', values)
        
        self.assertEqual(len(sg.values), 2)
        self.assertEqual(sg.values[0], values['a']['value'])
        self.assertEqual(sg.values[1], values['b']['value'])