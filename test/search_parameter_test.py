import unittest
from unittest.mock import Mock

from src.my_util import do_nothing
from src.browser.serach_parameter_container import SearchParameterContainer, SearchParameterPattern, SearchParameter

class NormalTest(unittest.TestCase):    
    def test_next_value(self):
        param = SearchParameter(
            xpath='XPATH',
            regex='REGEX',
            attribute_func=do_nothing
        )
        
        def __add_str(x, y):
            def __add(func):
                return [x + y]
            return __add
        
        result = list(param.next_values(__add_str)(do_nothing))
        self.assertEqual([param.xpath + param.regex], result)