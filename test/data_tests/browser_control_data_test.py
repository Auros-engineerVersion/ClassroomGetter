import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.data import *


class BrowserControlDataTest(unittest.TestCase):
    def test_create_driver_invailed_options(self):
        for option in [123456, None, type]:
            with self.subTest(msg=f'option: {option}', option=option), patch('src.interface.ISettingData') as cfg_mock:
                cfg_mock.web_driver_options.value = ['--headless', option]
                self.assertRaises(ValueError, create_driver, cfg_mock)
                
if __name__ == '__main__':
    unittest.main()