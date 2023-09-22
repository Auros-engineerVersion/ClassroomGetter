import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import MagicMock, patch

from src.data.serach_parameter_container import *
from src.my_util import identity


class ParameterTest(unittest.TestCase):
    def test_get_next_value(self):
        excepted = [0, 1, 2]
        param = SearchParameter(..., identity, identity)
        self.assertEqual(param.get_next_values(..., lambda x, y: [*range(3)]), excepted)
        
if __name__ == '__main__':
    unittest.main()