import os
import sys

sys.path.append(os.path.abspath('.'))

import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from src.gui.custum_widgets.info_boxes import *


class InputTest(unittest.TestCase):
    def test_set_and_get(self):
        root = tk.Tk()
        entry = EntryInput(master=root, title='a')
        spin = SpinInput(from_to=(1,1), master=root, title='b')
        dialog = DialogInput(master=root, title='c')
        
        inputs = {
            entry: 'test',
            spin: '1',
            dialog: 'NoData'}

        for input, value in inputs.items():
            with self.subTest(input=input, value=value):
                input.set(value)
                self.assertEqual(input.get(), value)
        
    def test_profileform(self):
        excepted = ('test_email', 'test_pass')
        form = ProfileForm()
        form.set(*excepted)
        self.assertTupleEqual(form.pop_up(lambda x: x.update()), excepted)