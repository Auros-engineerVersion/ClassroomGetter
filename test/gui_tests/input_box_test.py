import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
import tkinter as tk

from src.gui.custum_widgets.info_boxes import *

class InputTest(unittest.TestCase):
    def setUp(self) -> None:
        root = tk.Tk()
        self.__entry = EntryInput(root)
        self.__spin = SpinInput(root, from_to=(1,1))
        self.__dialog = DialogInput(root, default_path='NoData')
        
        self.__inputs: list[InputBox] = [
            [self.__entry, 'hoge'], 
            [self.__spin,   16],
            [self.__dialog, 'NoData']
        ]
        
    def test_is_current_value(self):
        for input, value in self.__inputs:
            with self.subTest(input=input, value=value):
                input.set(value)
                self.assertEqual(input.value(), value)
        
if __name__ == '__main__':
    unittest.main()