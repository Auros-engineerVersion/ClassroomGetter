import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk

from src.gui.custum_widgets import NodeBox
from src.data import Node
from src.handler import DriverSession


class NodeBoxTest(unittest.TestCase):
    def setUp(self) -> None:
        DriverSession.bc = MagicMock()
    
    def test_initialize(self):
        node = Node('key', 'url', 0)
        box = NodeBox(tk.Tk(), node)
        box.initialize((call_mock := MagicMock()))
        self.assertEqual(call_mock.call_count, 0)