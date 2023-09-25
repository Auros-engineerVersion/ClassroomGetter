import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
import json

from src.settings import *
from src.data import *


class JSONEncoderTest(unittest.TestCase):
    def __try_cast(self, x) -> int | str | list | Any:
        if isinstance(x, int):
            return int(x)
        else:
            if isinstance(x, list):
                return []
            else:
                return f'"{x}"' #ダブルクォーテーションで囲む
    
    def setUp(self) -> None:
        self.maxDiff = None
    
    def test_decode(self):
        key, url, tree_height = 'key', 'url', 0
        node = Node(key, url, tree_height)
        json_data = json.dumps(node.Nodes, cls=MyClassEncoder)
        
        vars = public_vars(node)
        excepted = [f'"{x[0]}": {self.__try_cast(x[1])}' for x in zip(vars.keys(), vars.values())]
        
        with self.subTest():
            for v in excepted:
                if 'next_init_time' in v or 'parent' in v:
                    continue
                else:
                    self.assertIn(v, json_data)
            
    def test_encode(self):
        node = Node('root_key', 'root_url', 0)
        node.add_edge(Node('child_key', 'child_url', 1))
        json_data = json.dumps(node, cls=MyClassEncoder, indent=4)
        after = json.loads(json_data, cls=MyClassDecoder)
        
        self.assertEqual(node, after)