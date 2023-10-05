import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch

from src.gui.application_root import ApplicationRoot
from src.my_io import *

class ApplicationRootTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_folder_path = Path('./for_test')
    
    @patch('src.gui.application_root.ProfileForm')
    def test_running_stop(self, form_mock):
        #Formを途中で終了した場合
        form_mock().pop_up.side_effect = [ChildProcessError]
        self.assertRaises(ChildProcessError, 
            ApplicationRoot, try_load(self.__test_folder_path), (400, 300))
        
    @patch('src.gui.application_root.ProfileForm')
    def test_run(self, form_mock):
        #ゲストモードで起動
        form_mock().pop_up.return_value = ('guest', 'guest')
        app = ApplicationRoot(try_load(self.__test_folder_path), (400, 300))
        app.stop()