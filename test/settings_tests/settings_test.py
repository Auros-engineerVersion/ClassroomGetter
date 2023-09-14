import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.my_util import arrow
from src.data import *
from src.setting import *


class SettingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_folder_path = Path('./test/for_settings_test')\
            |arrow| (lambda x: x.mkdir(parents=True, exist_ok=True))\
                
    def tearDown(self) -> None:
        self.__test_folder_path.joinpath('save.pkl')\
            |arrow| (lambda x: x.unlink(missing_ok=True))\
            |arrow| (lambda x: x.parent.rmdir())

    def test_save_and_load(self):
        self.assertRaises(TypeError, load, self.__test_folder_path)
        
        #読み書きできるか
        target_1 = SettingData(CommentableObj('いろはにほへと'))
        save(self.__test_folder_path, target_1)
        self.assertEqual(load(self.__test_folder_path), target_1)
        
        #上書き
        target_2 = SettingData(CommentableObj('ちりぬるお'))
        save(self.__test_folder_path, target_1)
        save(self.__test_folder_path, target_2)
        self.assertEqual(load(self.__test_folder_path), target_2)
        
    def test_try_load(self):
        self.assertIsInstance(try_load(self.__test_folder_path), SettingData)
        
    def test_no_such_file(self):
        self.assertRaises(TypeError, load, Path('.'))
        
    def test_save_node(self):
        target = SettingData()
        target.nodes = Node('key', 'url', 0).Nodes
        
        save(self.__test_folder_path, target)
        result = load(self.__test_folder_path)
        self.assertEqual(result, target)
        
        
if __name__ == '__main__':
    unittest.main()