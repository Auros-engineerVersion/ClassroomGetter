from __future__ import annotations

from src.interface.i_node import INode
from src.browser.browser_controls import BrowserControl as bc
from src.browser.serach_parameter_container import SearchParameterContainer

class Node(INode):
    #クラス変数の宣言と同時に定義を行わないのは、変数が勝手に起動してしまうため
    #つまり、BrowserControlはWebDrivreを有しているため、Chromeが勝手に起動してしまう
    BrowserControl: bc = None
    Nodes: set[INode] = set() #全てのノードの集合

    def __init__(self, key: str, url: str, tree_height: int) -> None:
        if Node.BrowserControl is None:
            raise TypeError('BrowserControl is None')
        
        self.__edges: set[INode] = set()
        self.key = key
        self.url = url
        self.tree_height = abs(tree_height) #負の値が入れられないように
        Node.Nodes.add(self)
    
    def __str__(self) -> str:
        return str.format('{0}:{1}', self.tree_height, self.key)
    
    def __lt__(self, other) -> bool:
        return self.tree_height < other.tree_height
    
    def __eq__(self, other) -> bool:
        if (other == None):
            return False
        else:
            return \
                self.tree_height == other.tree_height and\
                self.key         == other.key         and\
                self.url         == other.url         and\
                self.edges()     == other.edges()
    
    def __hash__(self) -> int:
        key_hash    = hash(self.key)
        url_hash    = hash(self.url)
        height_hash = hash(self.tree_height)
        
        return hash((key_hash, url_hash, height_hash))
    
    def __del__(self) -> None:
        if (self in Node.Nodes):
            Node.Nodes.remove(self)
            
        #それぞれのedgeから削除
        for node in Node.Nodes:
            if (self is node):
                continue
            
            if (self in node.edges()):
                node.edges().remove(self)
    
    #getter/setterを兼ねたもの
    def edges(self, add_value: INode = None) -> set[INode]:
        if add_value == None or add_value in self.__edges:
            return self.__edges
        else:
            self.__edges.add(add_value)
            Node.Nodes.add(add_value)
    
    def serach(self, bfs = True) -> INode:
        def __do_serch(func):
            list: list[INode] = [self]
            
            while(len(list) > 0):
                #出す場所が0なら幅優先探索, queueの振る舞いをする
                #何もないのであれば幅優先探索, stackの振る舞いをする
                value = list.pop(0) if bfs == True else list.pop()
                func(value)

                for child in value.edges():
                    list.append(child)
                    
        return __do_serch
                
    #幅優先探索
    def initialize_tree(root):
        def __next(node: INode):
            tuples = SearchParameterContainer.elements(node)
            for tuple in tuples:
                node.edges(
                    add_value=Node(*tuple, node.tree_height + 1)
                )
            
        root.serach()(__next)