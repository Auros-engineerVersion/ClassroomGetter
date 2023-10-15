import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
import json
from typing import Any

from src.my_io import *
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
        return super().setUp()
        
    def tearDown(self) -> None:
        Node.Nodes.clear()
        return super().tearDown()
    
    def test_encode_routine_data(self):
        data = RoutineData()
        json_data = json.dumps(data, cls=MyClassEncoder)
        
        vars = public_vars(data)
        excepted = trim_dict(dict([(k, try_cast(v)) for k, v in zip(vars.keys(), vars.values())]))
        
        for v in excepted:
            self.assertIn(v, json_data)
    
    def test_encode_node(self):
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
            
    def test_decode_node(self):        
        n_0 = Node('n_0_key', 'n_0_url', 0, True, RoutineData())
        before_len = len(Node.Nodes)
        
        json_data = json.dumps(n_0, cls=MyClassEncoder, indent=4)
        after = json.loads(json_data, cls=MyClassDecoder)
        
        self.assertEqual(len(Node.Nodes), before_len)
        self.assertIsInstance(after, Node)
        self.assertEqual(n_0, after)
        self.assertEqual(n_0.id, after.id)
        
    def test_encode_setting_data(self):
        data = SettingData()
        json_data = json.dumps(data, cls=MyClassEncoder)
        
        vars = public_vars(data)
        excepted = trim_dict(dict([(k, try_cast(v)) for k, v in zip(vars.keys(), vars.values())]))
        
        for v in excepted:
            self.assertIn(v, json_data)
                
    def test_decode_setting_data(self):
        data = SettingData()
        json_data = json.dumps(data, cls=MyClassEncoder, indent=4)
        after: SettingData = json.loads(json_data, cls=MyClassDecoder)
        
        self.assertIsInstance(after, SettingData)
                
        self.assertIsInstance(after.user_email[VALUE], str)
        self.assertIsInstance(after.user_password[VALUE], str)
        self.assertIsInstance(after.save_folder_path[VALUE], Path)
        self.assertIsInstance(after.loading_wait_time[VALUE], int)
        self.assertIsInstance(after.web_driver_options[VALUE], str)