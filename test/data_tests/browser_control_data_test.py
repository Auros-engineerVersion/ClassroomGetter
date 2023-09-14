import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from pathlib import Path

from src.data import *


class BrowserControlDataTest(unittest.TestCase):
    def test_create_driver_invailed_options(self):
        profile_path = Path(__file__).parent.joinpath('test_browser/Profile 1')
        for option in [123456, None, type]:
            with self.subTest(msg=f'option: {option}', option=option):
                self.assertRaises(ValueError, create_driver, profile_path, *list(('--headless', option)))
                
if __name__ == '__main__':
    unittest.main()