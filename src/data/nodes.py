from __future__ import annotations
import asyncio
from typing import Coroutine, Callable

from src.data.routine_data import RoutineData
from src.interface.i_node import INode
from src.browser.browser_controls import BrowserControl as bc
from src.data.serach_parameter_container import SearchParameterContainer

class Node(INode):
    #クラス変数の宣言と同時に定義を行わないのは、変数が勝手に起動してしまうため
    #つまり、BrowserControlはWebDrivreを有しているため、Chromeが勝手に起動してしまう
    BrowserControl: bc = None
    Nodes: set[INode] = set() #全てのノードの集合

    def __init__(self, key: str, url: str, tree_height: int, next_init_time: RoutineData = None) -> None:
        if Node.BrowserControl is None:
            raise TypeError('BrowserControl is None')
        
        self.__edges: set[INode] = set()
        self.__key = key
        self.__url = url
        self.__tree_height = abs(tree_height) #負の値が入れられないように
        self.__next_init_time = next_init_time if next_init_time != None else RoutineData()
        Node.Nodes.add(self)
        
    @property
    def edges(self):
        return self.__edges
    
    def add_edge(self, node: INode) -> set[INode]:
        if node in self.__edges:
            return None
        else:
            self.__edges.add(node)
            Node.Nodes.add(node)
        
    @property
    def key(self):
        return self.__key
    
    @property
    def url(self):
        return self.__url
        
    @property
    def tree_height(self):
        return self.__tree_height
    
    @property
    def next_init_time(self):
        return self.__next_init_time
    
    def __str__(self) -> str:
        return str.format('{0}:{1}', self.__tree_height, self.__key)
    
    def __lt__(self, other) -> bool:
        return self.__tree_height < other.tree_height
    
    def __eq__(self, other) -> bool:
        if (other == None):
            return False
        else:
            return \
                self.tree_height == other.tree_height and\
                self.key         == other.key         and\
                self.url         == other.url         and\
                self.edges     == other.edges
    
    def __hash__(self) -> int:
        key_hash    = hash(self.key)
        url_hash    = hash(self.url)
        height_hash = hash(self.tree_height)
        
        return hash((key_hash, url_hash, height_hash))
    
    def __del__(self) -> None:
        self.dispose()
    
    def dispose(self) -> None:
        if (self in Node.Nodes):
            Node.Nodes.remove(self)
            
        #それぞれのedgeから削除
        for node in Node.Nodes:
            if (self is node):
                continue
            
            if (self in node.edges):
                node.edges.remove(self)
    
    def serach(self, bfs = True) -> Coroutine[Callable[[Callable], None]]:
        """
        Args:
            bfs (bool, optional): Trueなら幅優先探索、Falseなら深さ優先探索を行う
        """
        async def __do_serch(func):
            list: list[INode] = [self]
            
            while(len(list) > 0):
                #出す場所が0なら幅優先探索, queueの振る舞いをする
                #何もないのであれば幅優先探索, stackの振る舞いをする
                value = list.pop(0) if bfs == True else list.pop()
                await func(value)

                for child in value.edges:
                    list.append(child)
                    
        return __do_serch
                
    #幅優先探索
    async def initialize_tree(root):
        async def __next(node: INode):
            tuples = await SearchParameterContainer.elements(node)
            for tuple in tuples:
                node.add_edge(
                    add_value=Node(*tuple, node.tree_height + 1)
                )
            
        await root.serach()(__next)