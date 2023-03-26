import os
import sys
sys.path.append(os.pardir)
from src import controls
import unittest

class ControlsTest(unittest.TestCase):
    def setUp(self):
        profile_path = r'C:\Users\kkyan\Documents\Code\Projects\Application\Classroom\chromeData'
        profile_name = 'Profile 1'
        self.controls = controls.Controls(profile_path, profile_name)
        
    def test_lesson_links_return_current_value(self):
        self.controls.lesson_links()