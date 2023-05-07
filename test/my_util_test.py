import unittest
from unittest.mock import Mock

from src.my_util import *

class NormalTest(unittest.TestCase):
    def test_convert_to_tuple(self):
        x = [0, 1, 2]
        y = ['a', 'b', 'c']
        
        result = convert_to_tuple(x, y)
        self.assertEqual([(0, 'a'), (1, 'b'), (2, 'c')], result)
        
        result = convert_to_tuple([1], [2])
        self.assertEqual([(1, 2)], result)
        
    def test_mid(self):
        x = 0
        y = 1
        z = 2
        n = mid(x, y, z)
        self.assertEqual(y, n)
        
    def test_identity(self):
        x = 0
        y = identity(x)(do_nothing)
        self.assertEqual(x, y)