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
        self.__data = SettingData(loading_wait_time=CommentableObj(1))
        self.__bc = BrowserControlData(self.__data)
        move(self.__bc, TARGET_URL)
        
    def tearDown(self):
        del self.__bc
    
    def test_serch_elements(self):
        def elem_get(xpath):
            return search_element(self.__bc, xpath).get_attribute('id')
            
        current_xpath = '//div[@id="hoge"]'
        self.assertEqual(elem_get(current_xpath), 'hoge')
        
        invailed_xpath = randstr(10)
        self.assertRaises(ValueError, elem_get, invailed_xpath)
        
        timeout_xpath = '//div[@id="fuga"]'
        self.assertRaises(ValueError, elem_get, timeout_xpath)
    
    def test_elements_filter_test(self):
        target = ['1', identity, -3.000, 1024, 'hoge', 'fuga', '硫化水素']
        result = elems_sifter(target, identity, '[a-z]{4}')
        excepted = ['hoge', 'fuga']
        self.assertEqual(result, excepted)
        
    def test_download(self):        
        self.__bc.wait._poll = 0.1
        dummy_url = 'https://google.com'
        
        #ファイルのダウンロードが間に合わなかった場合
        self.assertRaises(TimeoutError, donwload, self.__bc, dummy_url, Path('./dont_exist.txt'), 1)
        
        #ファイルのダウンロードが完了した場合
        path_mock = MagicMock()
        path_mock.exists.side_effect = [False for _ in range(3)] + [True]
        self.assertIsInstance(donwload(self.__bc, dummy_url, path_mock, 1), path_mock.__class__)
        
if __name__ == '__main__':
    unittest.main()