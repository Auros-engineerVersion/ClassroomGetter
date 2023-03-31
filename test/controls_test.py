import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
import unittest.mock
import settings as cfg
from src.controls import Controls

class ControlsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.controls = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)
    
    def tearDown(self) -> None:
        del self.controls
    
    def test_get_current_hrefs(self):
        