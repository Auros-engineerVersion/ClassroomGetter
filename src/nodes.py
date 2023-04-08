from __future__ import annotations
import sys, os
sys.path.append(os.path.abspath('.'))

import settings as cfg
from src.controls import Controls
from src import my_util

class Node:
    BrowserControl = None
    Nodes = [] #全てのノードを列挙する
    #0番目が授業タブの全てのトピック, 1番目が各トピック, 2番目がファイルの正規表現
    Patterns = ['^.+/0/.{11,20}$', '.*tc.{10,20}$', '.*file/d/.*']

    def __init__(self, key: str, tree_height) -> None:
        self.__edges: list[Node] = []
        self.key = key
        self.tree_height = tree_height
            
        #クラス変数の宣言と同時に定義を行わないのは、変数が勝手に起動してしまうため
        #つまり、BrowserControlはWebDrivreを有しているため、Chromeが勝手に起動してしまう
        if (Node.BrowserControl == None):
            Node.BrowserControl = Controls(cfg.PROFILE_PATH, cfg.PROFILE_NAME)
        pass
    
    #getter/setterを兼ねたもの
    def edges(self, add_value: Node = None):
        if (add_value != None):
            self.__edges.append(add_value)
        
        return self.__edges
    
    @staticmethod
    def ShowTree(parent: Node):
        def __indent(indent_size: int):
            result: str = ''
            for i in range(0, indent_size):
                result += '    ' #半角スペース4つはpythonと同じインデントである
            return result
        
        if (parent == None):
            return
            
        offset = parent.tree_height
        print(__indent(offset) + parent.key)
        for node in parent.edges():
            Node.ShowTree(node)
            
    @staticmethod
    def InitializeTree(parent: Node, controls: Controls):
        if (parent.key == None):
            return None
        else:
            Node.BrowserControl.move(parent.key)
            hrefs = Node.BrowserControl.hrefs(Node.BrowserControl.wait, Node.Patterns[parent.tree_height])
            stack: list[Node] = []
            for href in hrefs:
                link = my_util.to_all_tab_path(href)
                child = Node(link, parent.tree_height + 1)
                parent.edges(add_value=child)
                Node.Nodes.append(child)
                stack.append(child)
                
            while(len(stack) > 0):
                Node.InitializeTree(stack.pop(), controls)
                        
if __name__ == '__main__':
    root = Node(cfg.TARGET_URL, 0)
    Node.InitializeTree(root, Node.BrowserControl)
    Node.ShowTree(root)
    
    
#   https://classroom.google.com/w/NjAyMzgxOTE0MDk0/t/all     
#       https://classroom.google.com/w/NjAyMzgxOTE0MDk0/tc/NTE4MjgyNDQwNTE0/t/all
#
#上のurlは作られたもの
#下は実際のもの
#   https://classroom.google.com/w/NjAyMzgxOTE0MDk0/t/all
#       https://classroom.google.com/w/NjAyMzgxOTE0MDk0/tc/NTE4MjgyNDQwNTE0
#
#並べてみてみる
#https://classroom.google.com/w/NjAyMzgxOTE0MDk0/tc/NTE4MjgyNDQwNTE0/t/all
#https://classroom.google.com/w/NjAyMzgxOTE0MDk0/tc/NTE4MjgyNDQwNTE0

#/t/allが余分である