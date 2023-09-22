import sys, os

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import Mock

from src.my_util import *


class DummyClass: pass

class MyUtilTest(unittest.TestCase):
    def test_left(self):
        x = 0
        y = left(x)(identity)
        self.assertEqual(x, y)
        
    def test_is_none(self):
        excepted = 1
        self.assertEqual(excepted, is_none(None, excepted))
        
        #両方ともNoneの場合
        self.assertEqual(None, is_none(None, None))
        
        #fail_caseが関数の場合
        self.assertEqual(excepted, is_none(None, lambda: excepted))
        
        
    def test_randstr(self):
        length = 10
        result = randstr(length)
        self.assertEqual(length, len(result))
        
    def test_infix(self):
        add = Infix(lambda x, y: x + y)
        x = 1
        result = x |add| x |add| x
        self.assertEqual(x*3, result)
        
        div = Infix(lambda x, y: x / y)
        x = 1
        self.assertRaises(ZeroDivisionError, lambda: x |div| 0)