import unittest
from unittest.mock import Mock

from src import my_util

class NormalTest(unittest.TestCase):
    def test_convert_to_tuple(self):
        x = [0, 1, 2]
        y = ['a', 'b', 'c']
        
        result = my_util.convert_to_tuple(x, y)
        self.assertEqual([(0, 'a'), (1, 'b'), (2, 'c')], result)
        
    def test_mid(self):
        x = 0
        y = 1
        z = 2
        n = my_util.mid(x, y, z)
        self.assertEqual(y, n)