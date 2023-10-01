import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch

from src.browser import BrowserControlData
from src.gui.application_root import ApplicationRoot
from src.settings.settings import SettingData, Settings


class ApplicationRootTest(unittest.TestCase):
    @patch('src.setting.settings.Settings.load')
    def test_setup(self, m_load):        
        m_load.return_value = SettingData()
        cfg, bc = ApplicationRoot.setup()
        
        #ポップアップを途中で閉じた場合
        