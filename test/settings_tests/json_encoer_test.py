import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
import json

from src.settings import MyClassEncoder
from src.data import *

class JSONEncoderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
    
    def test_encode(self):
        node = Node('root_key', 'root_url', 0, RoutineData())
        node.add_edge(Node('child_key', 'child_url', 1, RoutineData()))
            
        result = json.dumps(node.Nodes, cls=MyClassEncoder, indent=4)
        self.assertEqual(result, '')