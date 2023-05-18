import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, MagicMock
import asyncio

from src.my_util import do_nothing
from src.interface.i_node import INode
from src.data.serach_parameter_container import *

def add_str(x, y):
    async def __add(func):
        await asyncio.sleep(0.1)
        return [x + y]
    return __add

class ParameterTest(unittest.TestCase):    
    def test_next_value(self):
        param = SearchParameter(
            xpath='XPATH',
            regex='REGEX',
            attribute_func=do_nothing
        )

        result = asyncio.run(param.next_values(add_str)(do_nothing))
        self.assertEqual([param.xpath + param.regex], list(result))
        
class PatternTest(unittest.TestCase):
    def setUp(self):
        node_mock = MagicMock()
        node_mock.key.side_effect = [0,1,2,3,4]
        node_mock.BrowserControl.elements = add_str
        self.__node_mock = node_mock
        
        self.__pattern = SearchParameterPattern(
            'test',
            SearchParameter(
                'hoge',
                'huga',
                do_nothing
            ),
            SearchParameter(
                'HOGE',
                'HUGA',
                do_nothing
            )
        )
    
    def test_elements(self):       
        self.assertEqual(asyncio.run(self.__pattern.elements(self.__node_mock)), [('hogehuga', 'HOGEHUGA')])