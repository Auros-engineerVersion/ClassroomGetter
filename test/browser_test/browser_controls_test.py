import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, AsyncMock
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

from src.browser.browser_controls import *
from src.data.browser_control_data import BrowserControlData
from src.data.setting_data import SettingData
from src.browser.browser_controls import *
from src.my_util import do_nothing

class BrowserControlsTest(unittest.TestCase):
    def setUp(self):
        self.__data = SettingData(loading_wait_time=1)
        self.__bc = BrowserControlData(self.__data)
        move(self.__bc, 'https://tonari-it.com/scraping-test/')
        
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
        
        self.assertEqual(list(results), excepted_results)

    #@patch('selenium.webdriver.support.ui.WebDriverWait.until')
    #def test_elements_with_invalid_xpath(self, mock_wait):
    #    xpath = '//div[@class="invalid"]'
    #    pattern = ''
    #    mock_wait.side_effect = TimeoutException
    #    with self.assertRaises(TimeoutException):
    #        self.bc.elements(xpath, pattern)

    #@patch('selenium.webdriver.support.ui.WebDriverWait.until')
    #def test_elements_with_pattern(self, mock_wait):
    #    xpath = '//div[@class="test"]'
    #    pattern = '^[0-9]'
    #    elems = [1, 2, 3]
    #    mock_wait.return_value = elems
    #    self.assertEqual(self.bc.elements(xpath, pattern), [1, 2, 3])
        
if __name__ == '__main__':
    unittest.main()