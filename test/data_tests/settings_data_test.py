import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.data.setting_data import SettingData
from src.interface import INode, ISettingData
from src.my_util import CommentableObj


class SettingDataTest(unittest.TestCase):
    def test_constructor(self):
        data = SettingData()
        self.assertIsInstance(data.nodes, set)
        self.assertIsInstance(data.nodes.pop(), INode)
    
    def test_is_current(self):
        invailed_data1 = SettingData()
        self.assertFalse(invailed_data1.is_current_data())
        
        commentable_obj = CommentableObj('hoge')
        invailed_data2 = SettingData(commentable_obj, commentable_obj)
        self.assertFalse(invailed_data2.is_current_data())
        
        sets = set()
        sets.add('Hoge')
        sets.add('bar')
        current_data = SettingData(
            CommentableObj('hogehoge@gmail.com'),
            CommentableObj('hogehoge'),
            nodes=sets,
            save_folder_path=CommentableObj(Path('.')))
        self.assertTrue(current_data.is_current_data())