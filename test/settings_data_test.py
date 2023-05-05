import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, Mock

from src.data.setting_data import SettingData

class NormalTest(unittest.TestCase):
    def test_is_current(self):
        invailed_data1 = SettingData()
        self.assertFalse(invailed_data1.is_current_data())
        
        invailed_data2 = SettingData('hoge', 'hoge')
        self.assertFalse(invailed_data2.is_current_data())
        
        sets = set()
        sets.add('Hoge')
        sets.add('bar')
        current_data = SettingData('hogehoge@gmail.com', 'hogehoge', node_list=sets)
        self.assertTrue(current_data.is_current_data())