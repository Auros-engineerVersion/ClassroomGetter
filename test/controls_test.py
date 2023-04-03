import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, Mock
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

import settings as cfg
from src.controls import Controls

class ControlsTest(unittest.TestCase):
    
  @patch.object(WebElement, 'get_attribute')
  @patch.object(WebElement, 'get_attribute')
  @patch.object(WebElement, 'get_attribute')
  def test_get_current_hrefs(self, element_mock1, element_mock2, element_mock3):
    element_mock1.get_attribute.return_value = 'http://www.example.com'
    element_mock2.get_attribute.return_value = 'https://www.1234567890.com'
    element_mock3.get_attribute.return_value = 'http://www.!"#$%&()=~|{`*}*?_?>+`}.net/test+3'
          
    wait_mock = Mock(spec=WebDriverWait)
    wait_mock.until.return_value = [element_mock1, element_mock2, element_mock3]    
    
    hrefs = Controls.hrefs(wait_mock, 'example')
    self.assertEqual(len(hrefs), 1)
            
if __name__ == '__main__':
    unittest.main()