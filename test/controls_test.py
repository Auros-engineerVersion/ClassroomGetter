import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, Mock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from src.controls import Controls

class ControlsTest(unittest.TestCase):
    def setUp(self) -> None:
        element_mock1 = Mock(spec=WebElement)
        element_mock2 = Mock(spec=WebElement)
        element_mock3 = Mock(spec=WebElement)

        element_mock1.get_attribute.return_value = 'http://www.example.com'
        element_mock2.get_attribute.return_value = 'https://www.1234567890.com'
        element_mock3.get_attribute.return_value = 'http://www.!"#$%&()=~|{`*}*?_?>+`}.net/test+3'

        element_mocks = [element_mock1, element_mock2, element_mock3]

        wait_mock = Mock(spec=WebDriverWait)
        wait_mock.until.return_value = element_mocks
        self.__wait_mock = wait_mock
    
    def test_get_current_hrefs(self):
        #添え字が大きくなるほど、linkに該当する条件が増えていく
        patterns = ['example', 'com', '']
        
        for i in range(0, 2):
            with self.subTest():
                hrefs = Controls.hrefs(self.__wait_mock, patterns[i])
                self.assertEqual(len(hrefs), i + 1)
                
    #ファイルのpath, .com/*/にfileと書かれている
    #https://drive.google.com/file/d/10Rj5zc75hsisZi5hme363_Emc1B_4QGG/view?usp=drive_web&authuser=0
    #formのpath,     .com/*/にformと書かれている
    #https://docs.google.com/forms/d/e/1FAIpQLSfVxTt2ncnuiCyGLJc7xKN3zS4WDsBJKQ9JzlfqoRI-UZwmbQ/viewform?hr_submission=ChkIqMHooJAJEhAImuKWw_4QEgcI6qCs6KwPEAE&authuser=0
    
if __name__ == '__main__':
    unittest.main()