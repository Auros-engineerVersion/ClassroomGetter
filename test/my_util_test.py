import unittest
from unittest.mock import Mock

from src.my_util import *

class DummyClass: pass

class MyUtilTest(unittest.TestCase):
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
        
    def test_randstr(self):
        length = 10
        result = randstr(length)
        self.assertEqual(length, len(result))
        
    def test_iterable_depth(self):
        x = [0, 1, 2]
        result = iterable_depth(x)
        self.assertEqual(1, result)
        
        x = [0, [[1], 2]]
        result = iterable_depth(x)
        self.assertEqual(3, result)
        
    def test_pipe(self):
        x = 0
        result = pipe(x, lambda x: x + 1)
        self.assertEqual(1, result)