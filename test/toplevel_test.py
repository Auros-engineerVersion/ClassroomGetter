import unittest
from unittest.mock import MagicMock, patch

import main
from src.gui.application_root import ApplicationRoot
from src.setting import *


class ToplevelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_folder_path = Path('./for_test')
    
    @patch('src.gui.application_root.ProfileForm')
    def test_running_stop(self, form_mock):
        #Formを途中で終了した場合
        form_mock().pop_up.side_effect = [ChildProcessError]
        self.assertRaises(ChildProcessError, ApplicationRoot, try_load(self.__test_folder_path), (400, 300))
        
    #@patch('src.gui.application_root.ProfileForm')
    #def test_complete_running(self, form_mock):
    #    form_mock().pop_up.side_effect = [('guest', 'guest')]
    #    main.main()