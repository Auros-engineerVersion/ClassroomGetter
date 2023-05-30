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
        
    def test_identity(self):
        x = 0
        y = identity(x)(do_nothing)
        self.assertEqual(x, y)
        
    def test_ratio(self):
        x_y = (400, 300)
        a = 5
        self.assertEqual((80, 60), ratio(*x_y, a))
        
        a = 0
        self.assertEqual((0, 0), ratio(*x_y, a))