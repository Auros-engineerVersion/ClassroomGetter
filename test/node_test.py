import sys, os
sys.path.append(os.path.abspath('.'))

import unittest
from unittest.mock import patch, Mock

from src.nodes import Node
from src.controls import Controls

class NodeTest(unittest.TestCase):
    def test_edge_getter(self):
        parent = Node('parent', 0)
        child =  Node('child', 1)
        
        parent.edges(add_value=child)
        self.assertEqual(parent.edges()[0], child)
        
    def test_show_tree(self):
        parent = Node('parent', 0)
        child1 = Node('child1', 1) 
        child2 = Node('child2', 1) 
        gchild = Node('gchild', 2)
        
        parent.edges(child1)
        parent.edges(child2)
        child1.edges(gchild)
        
        Node.ShowTree(parent)
    
if __name__ == '__main__':
    unittest.main()