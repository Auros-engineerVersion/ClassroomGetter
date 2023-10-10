import sys, os

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import Mock
from typing import Callable

from src.my_util import *


class MyUtilTest(unittest.TestCase):
    def test_higher_order(self):
        @higher_order
        def f(x):
            return x + 1
        
        self.assertIsInstance(f(1), Callable)
        self.assertEqual(f(1)(), 2)
        
        mutable = [0, 1, 2, 3]
        @higher_order
        def mutable_add(arr, x):
            arr.append(x)
        
        mutable |pipe| mutable_add(mutable, 4) |pipe| mutable_add(mutable, 5)
        self.assertListEqual(list(range(len(mutable))), mutable)
            
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
        
        #関数の入れ子
        self.assertEqual(excepted, is_none(None, lambda:lambda: excepted))
        
    def test_public_vars(self):
        a, b, c, d = 1, 2, 3, 4
        arguments = {'a': a, 'b': b, '__c': c, 'temp_class__d': d}
        class_x = type('temp_class', (object, ), arguments)
        
        propertys = public_vars(class_x)
        self.assertEquals(propertys, {'a': a, 'b': b})
        
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
        
        #pipe
        mock = Mock()
        x = 2 |pipe| mock |pipe| mock
        self.assertEqual(mock.call_count, 2)
        
        #return None Function
        x = 'hoge' |pipe| print |pipe| (lambda: print('hoge'))
        self.assertEqual(x, None)
        
        #arrow
        x = [] |arrow| (lambda x: x.append(1)) |arrow| (lambda x: x.append(2))
        self.assertListEqual([1, 2], x)