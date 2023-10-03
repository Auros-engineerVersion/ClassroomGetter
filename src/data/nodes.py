from __future__ import annotations

from pathlib import Path
from typing import Callable, Coroutine

from ..interface import *
from .routine_data import RoutineData
from .serach_parameter_container import SearchParameterContainer
from .minimalist_db import *


class Node(INode, IComparable):
    Nodes: MinimalistDB = MinimalistDB()
    SearchDepth: int = 0

    def __init__(self, key: str, url: str, tree_height: int, next_init_time: RoutineData = None) -> None:        
        self.__id: MinimalistID = self.Nodes.add(self)
        
        self.__key = key
        self.__url = url
        
        self.__tree_height = abs(int(tree_height)) #負の値が入れられないように
        self.__next_init_time = next_init_time if next_init_time != None else RoutineData()
        
        self.__parent: MinimalistID = None
        self.__edges: list[INode] = []

    #これらの引数の並びは、__init__で定義されている変数群の並びと同じである必要がある
    @classmethod
    def factory(cls, id, key, url, tree_height, next_init_time, parent, edges):
        """Jsonから読み込んだデータを元にノードを作成するためのfactory"""
        node = cls(key, url, tree_height, next_init_time)
        node.id = id
        node.parent = parent
        node.edges = edges
        
        return node

#region property
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, other):
        self.__id = other
        
    @property
    def edges(self):
        return self.__edges
    
    @edges.setter
    def edges(self, other):
        self.__edges = other
        
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
    
    @property
    def parent(self):
        return self.__parent
    
    @parent.setter
    def parent(self, id: MinimalistID):
        self.__parent = id
#endregion
    
    def __str__(self) -> str:
        return str.format('{0}:{1}', self.__tree_height, self.__key)
    
    def __lt__(self, other) -> bool:
        return self.__tree_height < other.tree_height
    
    def __eq__(self, other) -> bool:
        if (other == None):
            return False
        else:
            return all([x[0] == x[1] for x in zip(vars(self).values(), vars(other).values())])

    def __hash__(self) -> int:
        return hash((self.__key, self.__url, self.__tree_height, self.__next_init_time))
    
    def __del__(self) -> None:
        self.dispose()
    
    def add_edge(self, id: MinimalistID | INode) -> list[INode]:
        #idにINodeを入れてしまった場合
        if isinstance(id, INode):
            return self.add_edge(id.id)
        
        if self.Nodes.get(id) is EmptyRecode:
            raise ValueError('ノードが存在しません')
        else:
            self.__edges.append(id)
            self.Nodes.get(id)['value'].__parent = self.id
            
            return self.__edges
    
    def dispose(self) -> None:
        self.Nodes.remove(self.id)
            
        #それぞれのedgeから削除
        for recodes in self.Nodes:
            if isinstance(recodes, EmptyRecode):
                continue
            else:
                node: INode = recodes['value']
                if self is node:
                    continue

                if node.parent is not None and node.parent == self.id:
                    node.parent = None

                if self.id in node.edges:
                    node.edges.remove(self.id)
                    
    def to_path(self) -> Path:
        if len(Node.Nodes) == 0:
            raise ValueError('ノードが存在しません')
        
        getting: INode = lambda id: Node.Nodes.get(id)['value']
        
        def loop(id: MinimalistID):
            if id is None:
                return Path()
            else:
                return loop(getting(id).parent).joinpath(getting(id).key)
            
        return loop(self.id)
    
    def serach(self, bfs = True, search_depth: int = 0) -> Coroutine[Callable[[Callable], None]]:
        """
        Args:
            bfs (bool, optional): Trueなら幅優先探索、Falseなら深さ優先探索を行う
        """
        zero_to_neg = lambda x: -1 if x == False else 0
        popping = lambda list, bfs: Node.Nodes.get(list.pop(bfs))['value']
        
        def __do_serch(func):
            nonlocal search_depth
            list: list[INode] = [self.id]
            
            while(len(list) > 0):
                #出す場所が0なら深さ優先探索, queueの振る舞いをする
                #何もないのであれば幅優先探索, stackの振る舞いをする
                x =  zero_to_neg(bfs)
                node = popping(list, x)

                if search_depth > 0:
                    search_depth -= 1
                    func(node)
                    list.extend(node.edges)
                    
        return __do_serch
                
    #幅優先探索
    def initialize_tree(self) -> None:
        def __next(node: INode):
            for key, url in SearchParameterContainer.next_key_url(node):
                node.add_edge(Node(key, url, node.tree_height + 1))
            
        self.serach(search_depth=Node.SearchDepth)(__next)