import sys, os
sys.path.append(os.path.abspath('.'))

import settings as cfg
from src.controls import Controls
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestControls(unittest.TestCase):
    def setUp(self) -> None:
        self.controls = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)
        return super().setUp()
    
    def tearDown(self) -> None:
        del self.controls
        return super().tearDown()

    def test_can_move(self):
        self.controls.move(cfg.TARGET_URL)
        self.assertEqual(self.controls._driver.current_url, cfg.TARGET_URL)
        
    def test_links(self):
        self.controls.move(cfg.TARGET_URL)
        self.controls.lesson_links(cfg.LESSON_CLASS_NAME)
        self.assertTrue(True)
                
try:
    if __name__ == '__main__':
        unittest.main()
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    print(e)
    print('\033[0m')