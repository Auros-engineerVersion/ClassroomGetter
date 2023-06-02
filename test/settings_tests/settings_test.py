import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, Mock
from pathlib import Path

from src.setting.settings import Settings, SettingData

class SettingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_folder_path = Path('./test/for_settings_test')
        self.__test_folder_path.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self.__test_folder_path.joinpath('save.pkl').unlink(missing_ok=True)
        os.rmdir(self.__test_folder_path)

    def test_save_and_load(self):
        target_1 = SettingData('いろはにほへと')
        target_2 = SettingData('ちりぬるお')
        
        Settings.save(self.__test_folder_path, target_1)
        result = Settings.load(self.__test_folder_path)
        self.assertEqual(result, target_1)
        
        #上書き
        Settings.save(self.__test_folder_path, target_1)
        Settings.save(self.__test_folder_path, target_2)
        result = Settings.load(self.__test_folder_path)
        self.assertEqual(result, target_2)
        
    def test_no_such_file(self):
        self.assertEqual(Settings.load(self.__test_folder_path), SettingData())
    
if __name__ == '__main__':
    unittest.main()