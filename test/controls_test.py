import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, Mock
from src.controls import Controls

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class ControlsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__test_html = '''
<!DOCTYPE html>
<html>
  <head>
    <title>Example Page</title>
  </head>
  <body>
    <h1>Example Page</h1>
    <p>This is an example page with three links:</p>
    <ul>
      <li><a href="https://www.example1.com">Example Link 1</a></li>
      <li><a href="https://www.example2.com">Example Link 2</a></li>
      <li><a href="https://www.example3.com">Example Link 3</a></li>
    </ul>
  </body>
</html>
        '''

    @patch.object(WebDriverWait, 'until', return_value=[\
        '<a href="https://www.examples.com">Example Link 1</a>',\
        '<a href="https://www.12456790.com">Example Link 2</a>',\
        '<a href="https://www.HogeHoge.com">Example Link 3</a>'])
    def test_get_current_hrefs(self, wait_mock):
        hrefs = Controls.hrefs(wait_mock, 'examples')
        self.assertEqual(len(hrefs), 1)
            
if __name__ == '__main__':
    unittest.main()