import sys, os
sys.path.append(os.path.abspath('.'))

import settings
from src.controls import Controls
import unittest

class TestControls(unittest.TestCase):
    def setUp(self):
        self.controls = Controls(settings.PROFILE_PATH, settings.PROFILE_NAME)
        
if __name__ == '__main__':
    unittest.main()