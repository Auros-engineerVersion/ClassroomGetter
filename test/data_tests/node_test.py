import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import MagicMock
from random import randint

from src.data.nodes import *
from src.browser.browser_controls import *

class NodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__bc_mock = MagicMock(spec=BrowserControlData)
        Node.BrowserControl = self.__bc_mock
    
    def tearDown(self) -> None:
        while len(Node.Nodes) > 0:
            Node.Nodes.pop()
            
    def test_eq(self):
        x = Node('key', 'url', 0)
        self.assertEqual(x, x)
        
        y = Node('hoge', 'hoge', 1)
        self.assertNotEqual(x, y)
        
        z = Node('key', 'url', 0)
        self.assertEqual(x, z)
    
    def test_edges(self):
        parent = Node('parent', 'parent', 0)
        child =  Node('child', 'child', 1)
        
        parent.add_edge(child)
        self.assertIn(child, parent.edges)

        grandchild = Node('grandchild', 'grandchild', 2)
        child.add_edge(grandchild)
        self.assertIn(grandchild, child.edges)
        
        self.assertCountEqual(Node.Nodes, [parent, child, grandchild])
        
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
                
    def test_parent(self):
        parent = Node('parent', 'parent', 0)
        self.assertIsNone(parent.parent)
        
        child = Node('child', 'child', 1)
        parent.add_edge(child)
        self.assertEqual(child.parent, parent)
        
        parent.dispose()
        self.assertIsNone(child.parent)
    
    def test_search(self):
        root = Node('key_0', 'url_0', 0)
        range(randint(1, 10))
        for x in [Node(f'key_{i}', f'url_{i}', i) for i in range(2)]:
            root.add_edge(x)
        
        call_mock = MagicMock()
        root.serach()(call_mock)
        
        #すべての配列において呼び出しが発生しているかどうか
        self.assertEqual(call_mock.call_count, len(Node.Nodes) - 1)
        
    def test_null_controls(self):
        self.assertRaises(TypeError, Node, 'hoge', 0)
            
    def test_to_path(self):        
        root = Node('root', 'root', 0)
        stem = Node('stem', 'stem', 1)
        reaf = Node('reaf', 'reaf', 2)
        
        root.add_edge(stem)
        stem.add_edge(reaf)

        self.assertEqual(reaf.to_path(), Path('root/stem/reaf'))
        
        root.dispose()
        self.assertEqual(reaf.to_path(), Path('stem/reaf'))
        
        branch = Node('branch', 'branch', 2)
        stem.add_edge(branch)
        fruit = Node('fruit', 'fruit', 3)
        branch.add_edge(fruit)
        
        self.assertEqual(fruit.to_path(), Path('stem/branch/fruit'))