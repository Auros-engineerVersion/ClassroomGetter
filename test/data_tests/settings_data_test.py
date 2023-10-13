import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from pathlib import Path

from src.data import Node, SettingData
from src.interface import INodeProperty


class SettingDataTest(unittest.TestCase):
    def tearDown(self) -> None:
        Node.Nodes.clear()
        return super().tearDown()
    
    def test_constructor(self):
        data1 = SettingData()
        self.assertIsInstance(data1.nodes, list)
        self.assertIsInstance(*data1.nodes.pop().values(), INodeProperty)
        self.assertEqual(data1.search_depth['value'], Node.SearchDepth)
        
        data2 = SettingData('test', 'test')
        self.assertIsInstance(data2.user_email, dict)
    
    def test_is_current_nodes(self):
        invailed_data = SettingData()
        self.assertFalse(invailed_data.is_current_nodes())
        
        sets = set()
        sets.add('Hoge')
        sets.add('bar')
        current_data = SettingData(nodes=sets)
        self.assertTrue(current_data.is_current_nodes())
        
    def test_is_current_user(self):
        invailed_data1 = SettingData()
        self.assertFalse(invailed_data1.is_current_user())
        
        invailed_data2 = SettingData('@', 'admin')
        self.assertTrue(invailed_data2.is_current_user())

    def test_is_default(self):
        self.assertTrue(SettingData().is_default())
        
        data1 = SettingData('test', 'test')
        self.assertFalse(data1.is_default())

    def test_is_current(self):
        invailed_data1 = SettingData()
        self.assertFalse(invailed_data1.is_current_data())
        
        invailed_data2 = SettingData('@', 'admin')
        self.assertFalse(invailed_data2.is_current_data())
        
        sets = set()
        sets.add('Hoge')
        sets.add('bar')
        current_data = SettingData('hogehoge@gmail.com', 'hogehoge', Path(), 0, nodes=sets)
        self.assertTrue(current_data.is_current_data())
        
    def test_editable_data(self):
        data = SettingData()
        for v in data.normal.values():
            self.assertIsInstance(v, dict)