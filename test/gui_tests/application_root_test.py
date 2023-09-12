import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch

from src.gui.application_root import ApplicationRoot
from src.setting.settings import SettingData, Settings
from src.browser import BrowserControlData

class ApplicationRootTest(unittest.TestCase):
    @patch('src.setting.settings.Settings.load')
    def test_setup(self, m_load):        
        m_load.return_value = SettingData()
        cfg, bc = ApplicationRoot.setup()
        
        #ポップアップを途中で閉じた場合
        