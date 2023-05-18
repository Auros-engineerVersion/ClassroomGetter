import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import Mock, AsyncMock
from random import randint
import asyncio

from src.data.nodes import Node
from src.browser.browser_controls import BrowserControl

class NormalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__bc_mock = Mock(spec=BrowserControl)
        Node.BrowserControl = self.__bc_mock
    
    def tearDown(self) -> None:
        while len(Node.Nodes) > 0:
            Node.Nodes.pop()
    
    def test_edges(self):
        parent = Node('parent', 'parent', 0)
        child =  Node('child', 'child', 1)
        
        parent.add_edge(child)
        self.assertEqual(parent.edges.pop(), child)
        
    def test_destructor(self):
        def __create():
            parent = Node('parent', 'parent', 0)
            child = Node('child', 'child', 1)
            parent.add_edge(child)
            
            return (parent, child)
            
        nodes = __create()
        for target_node in nodes:
            with self.subTest(target_node.key + ' delete'):
                target_node.dispose()

                #全体集合から削除されているかどうか
                self.assertNotIn(target_node, Node.Nodes)
    
    def test_search(self):
        root = Node('key_0', 'uel_0', 0)
        list(map(
            root.add_edge,
            [Node(f'key_{i}', f'url_{i}', i) for i in range(randint(1, 10))]
        ))
        
        call_mock = AsyncMock()
        asyncio.run(root.serach()(call_mock))
        
        #すべての配列において呼び出しが発生しているかどうか
        self.assertEqual(call_mock.call_count, len(Node.Nodes))
        
class AbNormalTest(unittest.TestCase):
    def test_null_controls(self):
            self.assertRaises(TypeError, Node, 'hoge', 0)