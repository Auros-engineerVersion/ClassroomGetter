import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, MagicMock

from src.browser.browser_controls import *
from src.data import *
from src.my_util import identity, arrow

#このページは有志の方が作成されたスクレイピングテスト用のページです。
TARGET_URL = 'https://tonari-it.com/scraping-test/'

class BrowserControlsTest(unittest.TestCase):
    def setUp(self):
        self.__data = SettingData(loading_wait_time=1)
        self.__bc = BrowserControlData(self.__data)
        move(self.__bc, TARGET_URL)
        
    def tearDown(self):
        del self.__bc
    
    def test_serch_elements(self):
        def elem_get(xpath):
            return search_element(self.__bc, xpath).get_attribute('id')
            
        current_xpath = '//div[@id="hoge"]'
        self.assertEqual(elem_get(current_xpath), 'hoge')
        
        invailed_xpath = 'hogehoge'
        self.assertRaises(ValueError, elem_get, invailed_xpath)
        
        timeout_xpath = '//div[@id="fuga"]'
        self.assertRaises(ValueError, elem_get, timeout_xpath)
    
    def test_elements_filter_test(self):
        target = ['1', identity, -3.000, 1024, 'hoge', 'fuga', '硫化水素']
        result = elems_sifter(target, identity, '[a-z]{4}')
        excepted = ['hoge', 'fuga']
        self.assertEqual(result, excepted)
        
if __name__ == '__main__':
    unittest.main()