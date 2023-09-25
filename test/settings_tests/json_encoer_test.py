import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
import json

from src.settings import *
from src.data import *


def try_cast(x) -> int | str | list | Any:
    if isinstance(x, int):
        return int(x)
    else:
        if isinstance(x, list):
            return []
        else:
            return f'"{x}"' #ダブルクォーテーションで囲む

class JSONEncoderTest(unittest.TestCase):    
    def setUp(self) -> None:
        self.maxDiff = None
    
    def test_decode(self):
        key, url, tree_height, date = 'key', 'url', 0, RoutineData()
        node = Node(key, url, tree_height, date)
        json_data = json.dumps(node.Nodes, cls=MyClassEncoder)
        
        vars = public_vars(node)
        excepted = trim_dict(dict([(k, try_cast(v)) for k, v in zip(vars.keys(), vars.values())]))
        
        for v in excepted:
            if 'next_init_time' in v or 'parent' in v:
                continue
            else:
                self.assertIn(v, json_data)
            
    def test_encode(self):
        node = Node('root_key', 'root_url', 0, RoutineData())
        node.add_edge(Node('child_key', 'child_url', 1))
        json_data = json.dumps(node, cls=MyClassEncoder, indent=4)
        after = json.loads(json_data, cls=MyClassDecoder)
        
        self.assertEqual(node, after)
        self.assertIn(node, after.Nodes)