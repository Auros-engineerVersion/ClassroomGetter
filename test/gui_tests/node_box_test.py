import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk

from src.gui.custum_widgets import NodeBox
from src.data import *


class NodeBoxTest(unittest.TestCase):
    def setUp(self) -> None:
        SearchParameterContainer.browser_control_data = MagicMock()
    
    def test_initialize(self):
        node = Node('key', 'url', 0)
        box = NodeBox(tk.Tk(), node)
        box.initialize()