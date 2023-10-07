import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from pathlib import Path
from unittest.mock import MagicMock

from src.my_util import splitparN
from src.data import Node, EmptyRecode, MinimalistID


class NodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.n_gen = lambda i: Node(f'key_{i}', f'url_{i}', i)
    
    def tearDown(self) -> None:
        Node.Nodes.clear()
        return super().tearDown()
    
    def test_constructor(self):
        id_1 = Node('key', 'url', 0)
        self.assertIsNotNone(id_1)
        self.assertEqual(id_1.id, 0)
        
        id_2 = Node('key', 'url', 0)
        self.assertEqual(id_2.id, 1)
            
    def test_eq(self):
        x = Node('key', 'url', 0)
        self.assertEqual(x, x)
        
        y = Node('hoge', 'hoge', 1)
        self.assertNotEqual(x, y)
        
        #idが異なるため
        z = Node('key', 'url', 0)
        self.assertNotEqual(x, z)
    
    def test_edges(self):
        parent = Node('parent', 'parent', 0)
        child =  Node('child', 'child', 1)
        
        parent.add_edge(child.id)
        self.assertIn(child, parent.edges)

        grandchild = Node('grandchild', 'grandchild', 2)
        child.add_edge(grandchild)
        self.assertIn(grandchild, child.edges)
        
        self.assertEqual(len(Node.Nodes), 3)
        
    def test_raw_edges(self):
        n_0 = self.n_gen(0)
        n_1 = self.n_gen(1)
        n_1.add_edge(n_0)
        
        self.assertIsInstance(n_1.edges[0], MinimalistID)
        self.assertIsInstance(n_1.raw_edges[0], Node)
        
    def test_parent(self):
        parent = Node('parent', 'parent', 0)
        self.assertIsNone(parent.parent)
        
        child = Node('child', 'child', 1)
        parent.add_edge(child)
        self.assertEqual(child.parent, parent.id)
        
    def test_destructor(self):
        def node_env_set():
            Node.Nodes.clear()
            n_1 = self.n_gen(0)
            n_1.add_edge(n_2 := self.n_gen(1))
            n_2.add_edge(n_3 := self.n_gen(2))
            n_3.add_edge(n_4 := self.n_gen(3))
        
        #n_0を削除
        node_env_set()
        Node.Nodes[0]['value'].dispose()
        self.assertIsInstance(Node.Nodes[0], EmptyRecode)
        self.assertIsNone(Node.Nodes[1]['value'].parent)
        
        #中間を削除
        node_env_set()
        Node.Nodes[1]['value'].dispose()
        self.assertIsInstance(Node.Nodes[1], EmptyRecode)
        self.assertCountEqual(Node.Nodes[0]['value'].edges, [])
        self.assertIsNone(Node.Nodes[2]['value'].parent)
        
        #末端を削除
        node_env_set()
        Node.Nodes[3]['value'].dispose()
        self.assertIsInstance(Node.Nodes[3], EmptyRecode)
        self.assertCountEqual(Node.Nodes[2]['value'].edges, [])
    
    def test_search(self):
        n_0 = self.n_gen(0)
        n_0.add_edge(n_1 := self.n_gen(1))
        n_1.add_edge(n_2 := self.n_gen(2))
        n_2.add_edge(n_3 := self.n_gen(3))
        
        search_depthes = [0, 2, 10] #どこまで探索するか
        for depth in search_depthes:
            with self.subTest(depth=depth):
                call_mock = MagicMock()
                n_0.serach(search_depth=depth)(call_mock)
                
                if len(Node.Nodes) > depth:
                    self.assertEqual(call_mock.call_count, depth)
                else:
                    #search_depthがtreeの長さを超えている場合
                    self.assertEqual(call_mock.call_count, len(Node.Nodes))
        
    def test_null_controls(self):
        self.assertRaises(TypeError, Node, 'hoge', 0)
            
    def test_to_path_when_include_true(self):
        root = Node('root', 'root', 0, include_this_to_path=True)
        stem = Node('stem', 'stem', 1, include_this_to_path=True)
        reaf = Node('reaf', 'reaf', 2, include_this_to_path=True)
        
        root.add_edge(stem)
        stem.add_edge(reaf)

        self.assertEqual(reaf.to_path(), Path('root/stem/reaf'))
        
        root.dispose()
        self.assertEqual(reaf.to_path(), Path('stem/reaf'))
        
        branch = Node('branch', 'branch', 2, True)
        stem.add_edge(branch)
        fruit = Node('fruit', 'fruit', 3, True)
        branch.add_edge(fruit)
        
        self.assertEqual(fruit.to_path(), Path('stem/branch/fruit'))
        
    def test_to_path_when_include_false(self):
        n_0 = self.n_gen(0)
        n_0.add_edge(n_1 := self.n_gen(1))
        n_1.add_edge(n_2 := self.n_gen(2))
        n_2.add_edge(n_3 := self.n_gen(3))
        
        #全てがFalseの場合
        self.assertEqual(n_3.to_path(), Path('.'))
        
        n_0.include_this_to_path = True
        n_1.include_this_to_path = False
        n_2.include_this_to_path = True
        n_3.include_this_to_path = True
        
        self.assertEqual(n_3.to_path(), Path('key_0/key_2/key_3'))
        
        n_0.include_this_to_path = False
        self.assertEqual(n_3.to_path(), Path('key_2/key_3'))
        
if __name__ == '__main__':
    unittest.main()