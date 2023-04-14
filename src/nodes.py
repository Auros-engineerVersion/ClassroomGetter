from __future__ import annotations
import sys, os
sys.path.append(os.path.abspath('.'))
from selenium.webdriver.common.by import By

from src import my_util
from interface.i_node import INode
from browser_controls import BrowserControls as bc

class Node(INode):
    #クラス変数の宣言と同時に定義を行わないのは、変数が勝手に起動してしまうため
    #つまり、BrowserControlはWebDrivreを有しているため、Chromeが勝手に起動してしまう
    BrowserControl: bc = None
    Nodes: set[INode] = set() #全てのノードの集合

    def __init__(self, key: str, tree_height: int) -> None:
        if Node.BrowserControl is None:
            raise TypeError('BrowserControl is None')
        
        self.__edges: list[INode] = []
        self.key = key 
        self.tree_height = abs(tree_height) #負の値が入れられないように
        Node.Nodes.add(self)
        pass
    
    def __del__(self):
        Node.Dispose(self)
    
    def __str__(self) -> str:
        return str.format('{0}:{1}', self.tree_height, self.key)
    
    #getter/setterを兼ねたもの
    def edges(self, add_value: INode = None) -> list[INode]:
        if (add_value != None):
            self.__edges.append(add_value)
            Node.Nodes.add(add_value)
        
        return self.__edges
    
    def next_links(self) -> list[str]:
        c = self.BrowserControl

        #ホームなら
        if (self.tree_height == 0):
            c.move(self.key)
            locator = (By.XPATH, "//a[@class='onkcGd ZmqAt Vx8Sxd']")
            pattern = '^.*/u/./c/.{16}$'
            return c.hrefs()(locator, pattern)
        #授業のタブなら
        elif ('/u/0/c' in self.key):
            return [my_util.to_all_tab_link(self.key)]
        
        #「全てのトピック」なら
        elif ('/t/all' in self.key):
            c.move(self.key)
            locator = (By.XPATH, "//a[@class='VkhHKd e7EEH ']")
            pattern = '^.*/file/d/.*$'
            return c.click_all_sections(c.hrefs, (locator, pattern))
        
        #ファイルのurlなら
        else:
            return []
            
    def create_childs(self, *keys: str):
        for key in keys:
            child = Node(key, self.tree_height + 1)
            self.edges(child)
            
        return self
    
    #HACK: インスタンスメソッドにした方が簡潔
    @staticmethod
    def Dispose(target: INode):
        #全体の集合から削除
        if (target in Node.Nodes):
            Node.Nodes.remove(target)
            
        #それぞれのedgeから削除
        for node in Node.Nodes:
            if (target in node.edges()):
                node.edges().remove(target)

    @staticmethod
    def ShowTree(parent: INode):
        def __indent(indent_size: int):
            result: str = ''
            for i in range(indent_size):
                result += '    ' #半角スペース4つはpythonと同じインデントである
            return result
        
        if (parent == None):
            return
        
        print(__indent(parent.tree_height) + str(parent))
        
        for node in parent.edges():
            Node.ShowTree(node)
                
    #幅優先探索
    @staticmethod
    def InitializeTree(parent: INode):            
        queue: list[Node] = [parent]
                
        while (len(queue) > 0):
            value = queue.pop(0)
            links = value.next_links()
            
            if (len(links) > 0):
                value.create_childs(*links)
                
            for child in value.edges():
                queue.append(child)