import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, Mock

from src.setting.settings import Settings

class NormaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_file_path = './test/for_test.pkl'
        open(self.__test_file_path, 'w')
        return super().setUp()

    def tearDown(self) -> None:
        os.remove(self.__test_file_path)
        return super().tearDown()

    def test_Save_and_Load(self):
        target_1 = [*'いろはにほへと']
        target_2 = [*'ちりぬるお']
        Settings.Save(self.__test_file_path, *target_1)
        result = Settings.Load(self.__test_file_path)
        
        self.assertEqual(result, target_1)
        
        Settings.Save(self.__test_file_path, *target_1)
        Settings.Save(self.__test_file_path, *target_2)
        result = Settings.Load(self.__test_file_path)
        
        self.assertEqual(result, target_2)
    
class AbNormalTest(unittest.TestCase):
    def test_constructor(self):
        self.assertRaises(ValueError, Settings, 'HogeHoge')
        
if __name__ == '__main__':
    unittest.main()