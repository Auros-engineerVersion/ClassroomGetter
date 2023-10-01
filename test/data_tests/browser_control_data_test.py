import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest

from src.data.browser_control_data import *
from src.data.setting_data import *


class BrowserControlDataTest(unittest.TestCase):    
    def test_create_driver(self):
        driver = create_driver(SettingData())
        c_info = driver.__dict__['caps']['chrome']
        
        #Version check
        with self.subTest('Chrome Version'):
            self.assertGreater(int(c_info['chromedriverVersion'].split('.')[0]), 116)
        
        with self.subTest('Profile Exist Check'):
            self.assertTrue(os.path.exists(c_info['userDataDir']))