import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, AsyncMock
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from re import search
import asyncio

from src.data.setting_data import SettingData
from src.browser.browser_controls import *
from src.my_util import do_nothing

class BrowserControlsTest(unittest.TestCase):    
    def test_elements_with_valid_xpath(self):
        xpath = '//div[@class="test"]'
        pattern = ''
        elems = [1, 2, 3]
        
        bc = BrowserControl(SettingData())
        self.assertEqual(asyncio.run(elements(bc, xpath, pattern)(do_nothing)), elems)

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