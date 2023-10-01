import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import MagicMock, patch

from src.data.serach_parameter_container import *
from src.my_util import identity, arrow


class ParameterTest(unittest.TestCase):
    def test_get_next_value(self):
        excepted = [0, 1, 2]
        param = SearchParameter(..., identity, identity)
        self.assertEqual(param.get_next_values(..., lambda x, y: [*range(3)]), excepted)
        
class SearchParameterContainerTest(unittest.TestCase):
    def setUp(self) -> None:
        SearchParameterContainer.browser_control_data = MagicMock()
        self.spc = SearchParameterContainer
        return super().setUp()
    
    def test_level_2(self):
        node = MagicMock()
        node.url = 'https://classroom.google.com/u/1/c/AAAAAAAAAAAAAAAA'
        node.key = 'test'
        node.tree_height = 1
        
        result = self.spc.next_key_url(node)
        
        self.assertTupleEqual(
            result,
            ('testの授業タブ', 'https://classroom.google.com/u/1/w/AAAAAAAAAAAAAAAA/t/all'))
        
    def test_level_4(self):
        node = MagicMock()
        node.url = 'https://drive.google.com/file/d/AAAAAAAAAAAAAAAA/view?usp=drive_web&authuser=1'
        node.key = 'test'
        node.tree_height = 4
        
        result = self.spc.next_key_url(node)
        self.assertIsNone(result)
        
if __name__ == '__main__':
    unittest.main()