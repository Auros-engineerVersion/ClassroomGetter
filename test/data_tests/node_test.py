import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import Mock

from data.nodes import Node
from src.browser.browser_controls import BrowserControl

class NormalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__bc_mock = Mock(spec=BrowserControl)
        Node.BrowserControl = self.__bc_mock
    
    def tearDown(self) -> None:
        while len(Node.Nodes) > 0:
            Node.Nodes.pop()
    
    def test_edge_getter(self):
        parent = Node('parent', 'parent', 0)
        child =  Node('child', 'child', 1)
        
        parent.edges(add_value=child)
        self.assertEqual(parent.edges().pop(), child)
        
    def test_destructor(self):
        def __create():
            parent = Node('parent', 'parent', 0)
            child = Node('child', 'child', 1)
            parent.edges(child)
            
            return (parent, child)
            
        nodes = __create()
        for target_node in nodes:
            with self.subTest(target_node.key + ' delete'):
                target_node.dispose()

                #全体集合から削除されているかどうか
                self.assertNotIn(target_node, Node.Nodes)
    
    def test_search(self):
        root = Node('0', '0', 0)
        childs = [Node('a', 'a', 1), Node('b', 'b', 1), Node('c', 'c', 1)]
        list(map(root.edges, childs))
        
        call_mock = Mock()
        root.serach()(call_mock)
        #すべての配列において呼び出しが発生しているかどうか
        self.assertEqual(call_mock.call_count, len(Node.Nodes))
        
class AbNormalTest(unittest.TestCase):
    def test_null_controls(self):
            self.assertRaises(TypeError, Node, 'hoge', 0)