import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, MagicMock
import asyncio
from random import randint

from src.my_util import do_nothing, randstr
from src.interface.i_node import INode
from src.data.serach_parameter_container import *

def add_str(x, y, z):
    def __add(func):
        return [x + y + z]
    return __add

def create_param(string_func, *args):
    return SearchParameter(
        xpath=string_func(*args),
        regex=string_func(*args),
        attribute_func=do_nothing
    )

def pattern_factory(create_count: int = 1):
    str_length = randint(5, 10)
    params: list[SearchParameterPattern] = []
    def __create(list: list, count: int):
        if count <= 0:
            return None
        else:
            list.append(
                SearchParameterPattern(
                    pattern_name=randstr(str_length),
                    text_param=create_param(randstr, str_length),
                    link_param=create_param(randstr, str_length)
                )
            )
            
            __create(list, count - 1)
            return list
        
    return __create(params, create_count)
                
def get_text_regex_str(param: SearchParameter):
    return param.xpath + param.regex
    
def get_from_pattern(pattern: SearchParameterPattern):
    return get_text_regex_str(pattern.text_param), get_text_regex_str(pattern.link_param)
    
class ParameterTest(unittest.TestCase):
    def test_next_value(self):
        bc = ''
        param = create_param(randstr, 10)

        result = param.next_values(bc)(do_nothing)(add_str)(do_nothing)
        self.assertEqual([bc + param.xpath + param.regex], list(result))
        
class ParameterPatternTest(unittest.TestCase):
    def test_name_elements_pair(self):
        bc = ''
        node = MagicMock()
        node.key = 'KEY'
        node.url = 'URL'
        
        patterns = pattern_factory(randint(1, 10))        
        result = map(lambda x: x.name_elements_pair(bc, node)(add_str, do_nothing), patterns)
        excepted_result = map(get_from_pattern, patterns)

        self.assertListEqual(sum(list(result), start=[]), list(excepted_result))