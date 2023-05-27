import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, MagicMock
import asyncio

from src.my_util import do_nothing
from src.interface.i_node import INode
from src.data.serach_parameter_container import *

def add_str(x, y, z):
    def __add(func):
        return [x + y + z]
    return __add

class ParameterTest(unittest.TestCase):    
    def test_next_value(self):
        bc = 'BC'
        param = SearchParameter(
            xpath='XPATH',
            regex='REGEX',
            attribute_func=do_nothing
        )

        result = param.next_values(bc)(add_str)(do_nothing)
        self.assertEqual([bc + param.xpath + param.regex], list(result))