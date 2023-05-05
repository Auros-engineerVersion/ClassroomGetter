import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, Mock
from pathlib import Path

from src.setting.settings import Settings, SettingData

class NormaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_folder_path = Path('./test/for_settings_test')
        return super().setUp()

    def tearDown(self) -> None:
        os.remove(self.__test_folder_path.joinpath('save.pkl'))
        os.rmdir(self.__test_folder_path)
        return super().tearDown()

    def test_save_and_load(self):
        target_1 = SettingData('いろはにほへと', setting_folder_path=self.__test_folder_path)
        target_2 = SettingData('ちりぬるお', setting_folder_path=self.__test_folder_path)
        
        Settings.save(target_1)
        result = Settings.load(self.__test_folder_path)
        self.assertEqual(result, target_1)
        
        #上書き
        Settings.save(target_1)
        Settings.save(target_2)
        result = Settings.load(self.__test_folder_path)
        self.assertEqual(result, target_2)
    
class AbNormalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_folder_path = Path('./test/for_settings_test')
        self.__test_folder_path.mkdir(parents=True, exist_ok=True)
        return super().setUp()

    def tearDown(self) -> None:
        os.rmdir(self.__test_folder_path)
        return super().tearDown()
    
    def test_no_such_file(self):
        self.assertEqual(Settings.load(self.__test_folder_path), SettingData())
    
if __name__ == '__main__':
    unittest.main()