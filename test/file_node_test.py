import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from src.file_node import FNode

class CustomConditionTest(unittest.TestCase):
    def test_return_current_path(self):
        fnode = FNode('3th', 'TempClass', '15th')
        self.assertEqual('3th/TempClass/15th', fnode.path())
        
if __name__ == '__main__':
    unittest.main()