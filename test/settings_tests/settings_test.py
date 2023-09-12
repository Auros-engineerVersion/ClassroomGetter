import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.setting import *

class SettingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_folder_path = Path('./test/for_settings_test')
        self.__test_folder_path.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self.__test_folder_path.joinpath('save.pkl').unlink(missing_ok=True)
        os.rmdir(self.__test_folder_path)

    def test_save_and_load(self):
        target_1 = SettingData('いろはにほへと')
        
        save(self.__test_folder_path, target_1)
        result = load(self.__test_folder_path)
        self.assertEqual(result, target_1)
        
        #上書き
        target_2 = SettingData('ちりぬるお')
        save(self.__test_folder_path, target_1)
        save(self.__test_folder_path, target_2)
        result = load(self.__test_folder_path)
        self.assertEqual(result, target_2)
        
    def test_no_such_file(self):
        self.assertEqual(load(self.__test_folder_path), SettingData())
        
    def test_setup_data(self):
        self.assertEqual(setup_data(MagicMock()), lambda x: x)
    
if __name__ == '__main__':
    unittest.main()