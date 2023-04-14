import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, Mock, MagicMock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from src.setting_data import SettingData
from src.browser_controls import BrowserControls

class NormalTest(unittest.TestCase):
    def setUp(self) -> None:
        test_urls = ['http://www.example.com', 'http://www.example.com', 'https://www.1234567890.com', 'http://www.!"#$%&()=~|{`*}*?_?>+`}.net/test+3']
        element_mocks = []
        for i in range(3):
            elem_mock = Mock(spec=WebElement)
            elem_mock.return_value = test_urls[i]
            element_mocks.append(elem_mock)

        self.__element_mocks = element_mocks
        
        #instanceの初期化
        driver_mock = MagicMock()
        wait_mock = MagicMock()
        settings = SettingData('http://www.example.com', 'hogehoge@example.com', 'admin', 1)
        self.__bc = BrowserControls(driver_mock, wait_mock, settings)

    @patch.object(WebDriverWait, 'until')
    def test_get_current_hrefs(self, wait_mock):
        wait_mock.return_value = self.__element_mocks
        
        elems = self.__bc.hrefs()((By.XPATH, 'Hoge'), 'example.com')
        
        self.assertEqual(elems.pop(), self.__element_mocks[0])
                
    #ファイルのpath, .com/*/にfileと書かれている
    #https://drive.google.com/file/d/10Rj5zc75hsisZi5hme363_Emc1B_4QGG/view?usp=drive_web&authuser=0
    #formのpath,     .com/*/にformと書かれている
    #https://docs.google.com/forms/d/e/1FAIpQLSfVxTt2ncnuiCyGLJc7xKN3zS4WDsBJKQ9JzlfqoRI-UZwmbQ/viewform?hr_submission=ChkIqMHooJAJEhAImuKWw_4QEgcI6qCs6KwPEAE&authuser=0
    
class AbNormalTest(unittest.TestCase):
    pass    

if __name__ == '__main__':
    unittest.main()