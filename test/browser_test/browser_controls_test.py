import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch

from src.browser.browser_controls import *
from src.data.browser_control_data import BrowserControlData
from src.data.setting_data import SettingData
from src.my_util import do_nothing

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
        xpathes = [
            '//div[@id="hoge"]',
            'qwryioplkjhgdsazxvnm',
            '//div[@class="13-.,,""@[]/;/"]'
        ]
        
        excepted_results = ['hoge', None, None]
        
        results = map(
            lambda elem: elem.get_attribute('id') if elem != None else None,
            map(lambda xpath: search_element(self.__bc, xpath), xpathes)
        )
        
        self.assertListEqual(list(results), excepted_results)
    
    def test_elements_filter_test(self):
        target = ['1', do_nothing, -3.000, 1024, 'hoge', 'fuga', '硫化水素']
        self.assertEqual(elements_filter(do_nothing, '[a-z]{4}')(target), ['hoge', 'fuga'])
        
if __name__ == '__main__':
    unittest.main()