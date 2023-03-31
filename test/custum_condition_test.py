import sys, os
sys.path.append(os.path.abspath('.'))

#region selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
#endregion

import unittest
from unittest.mock import patch, Mock, MagicMock
import time

from src import custum_condition as MyEC
import settings as cfg
from src.factory import create_driver

class CustomConditionTest(unittest.TestCase):
    #docment.readyStateは以下の三つの状態をとる
    #loading: この文書 (document) はまだ読み込み中
    #interactive: 文書の読み込みが完了したが、スクリプトなどのサブリソースはまだ読み込み中である。
    #complete: 文書とすべてのサブリソースの読み込みが完了した
    def test_document_state_is_can_wait(self):
        driver_mock = Mock(spec=webdriver.Chrome)
        mock_list = ['loading','loading','loading','interactive','interactive','interactive', 'complete']
        
        with patch.object(driver_mock, 'execute_script', side_effect=mock_list) as script_call:
            wait = WebDriverWait(driver_mock, 30)
            wait.until(MyEC.document_state_is((By.TAG_NAME, 'a'), 'complete'))
            
            self.assertEqual(script_call.call_count, len(mock_list))          