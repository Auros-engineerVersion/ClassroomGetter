import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import MagicMock, patch

from src.gui.custum_widgets import *


class SettingGroupTest(unittest.TestCase):
    def test_boxes(self):
        values = {'a': {'value': '1', 'description': 'a'}, 'b': {'value': '2', 'description': 'b'}}
        sg = SettingGroup(tk.Tk(), values)
        
        self.assertEqual(len(list(sg.boxes)), 2)
        for box, excepted in zip(sg.boxes, values.values()):
            with self.subTest(msg=f'{box}: {box.get()}', box=box):
                self.assertIsInstance(box, InputBox)
                self.assertEqual(box.get(), excepted['value'])