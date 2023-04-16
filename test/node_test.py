import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, Mock

from src.browser.nodes import Node
from src.browser.browser_controls import BrowserControls

class NormalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__bc_mock = Mock(spec=BrowserControls)
        Node.BrowserControl = self.__bc_mock
     
    def test_edge_getter(self):
        parent = Node('parent', 0)
        child =  Node('child', 1)
        
        parent.edges(add_value=child)
        self.assertEqual(parent.edges()[0], child)
    
    def test_create_child(self):
        str_nums = []
        for i in range(100):
            str_nums.append(str(i))
            
        parent = Node('0', 0)
        parent.create_childs(*str_nums)
        self.assertCountEqual(parent.edges(), str_nums)
        
    def test_Dispose(self):
        with self.subTest('Parent Dispose'):
            parent = Node('Hoge', 0)
            child = Node('Bar', 1)
            parent.edges(child)
        
            Node.Dispose(parent)
        
            #全体集合から削除されているかどうか
            self.assertEqual(len(Node.Nodes), 1)
            self.assertEqual(Node.Nodes.pop(), child)
            
        with self.subTest('Child Dispose'):
            parent = Node('Hoge', 0)
            child = Node('Bar', 1)
            parent.edges(child)
        
            Node.Dispose(child)
            
            #各nodeから削除対象への参照がきちんと削除されているかどうか
            self.assertEqual(len(parent.edges()), 0)
    
    @patch.object(Node, 'next_links')    
    def test_InitializeTree(self, next_mock):
        mock_list = [*'abcde', *'ABCDE', *'あいうえお', *'*}_?|', []]
        total_mock_list_size = 21
        next_mock.side_effect = mock_list
        
        root = Node('parent', 0)
        Node.InitializeTree(root)
        
        #すべての配列において呼び出しが発生しているかどうか
        self.assertEqual(next_mock.call_count, total_mock_list_size)
        
class AbNormalTest(unittest.TestCase):
    def test_null_controls(self):
            self.assertRaises(TypeError, Node, 'hoge', 0)