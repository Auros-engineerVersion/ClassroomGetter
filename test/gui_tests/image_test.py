import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import caputer

from my_util import *

IMAGE_PATH = Path('test/gui_tests/images')

class ImageTest(unittest.TestCase):
    def setUp(self) -> None:
        if not IMAGE_PATH.exists():
            IMAGE_PATH.mkdir()
        
    def test_caputuer(self):
        for cls in all_class_in_dir(Path('src/gui')):
            if 'src' in str(cls):
                caputer.caputuer(cls(), f'test/gui_tests/images/{cls}.png', overwrite=True)
                
if __name__ == '__main__':
    unittest.main()