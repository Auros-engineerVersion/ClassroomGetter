from __future__ import annotations

from pathlib import Path
from typing import Callable

from ..interface import *
from ..my_util import is_none
from .routine_data import RoutineData
from .minimalist_db import *


class Node(INodeProperty, IHasEdges, IDisposable):
    Nodes: MinimalistDB = MinimalistDB()
    SearchDepth: int = 0
    
    #これらの引数の並びは、__init__で定義されている変数群の並びと同じである必要がある
    #これはjsonから読み込んだデータを元にノードを作成する際に同じでないとうまくインスタンスの生成ができないため
    @classmethod
    def factory(cls, id, key, url, tree_height, include_this_to_path, next_init_time, parent, edges):
        """Jsonから読み込んだデータを元にノードを作成するためのfactory"""
        node = cls(key, url, tree_height, include_this_to_path, next_init_time)
        node.id = id
        node.parent = parent
        node.edges = edges
        
        return node
    
    @classmethod
    def root(cls) -> Node:
        return min(Node.Nodes, key=lambda x: x['value'].tree_height)['value']

    def __init__(self, key: str, url: str, tree_height: int, include_this_to_path: bool = False, next_init_time: RoutineData = None) -> None:
        self.__id: MinimalistID = self.Nodes.add(self)
        
        self.__key: str = key
        self.__url: str = url
        self.__tree_height: int = abs(int(tree_height))
        self.__include_this_to_path: bool = include_this_to_path
        self.__next_init_time: RoutineData = is_none(next_init_time, RoutineData)
        
        self.__parent: MinimalistID = None
        self.__edges: list[IHasEdges] = []

    def __str__(self) -> str:
        return str.format(self.__dict__)
    
    def __lt__(self, other) -> bool:
        return self.__tree_height < other.tree_height
    
    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, Node):
            return False
        else:
            argument_eq = []
            for key, x, y in zip(vars(self).keys(), vars(self).values(), vars(other).values()):
                if '_Node__id' in key:
                    continue
                else:
                    argument_eq.append(x == y)
            
            return all(argument_eq)

    def __hash__(self) -> int:
        return hash(vars(self).values())
    
    def __del__(self) -> None:
        self.dispose()

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, other):
        self.__id = other
        
#region INodeProperty
    @property
    def key(self) -> str:
        return self.__key
    
    @property
    def url(self) -> str:
        return self.__url
    
    @property
    def tree_height(self) -> int:
        return self.__tree_height
    
    @property
    def next_init_time(self) -> RoutineData:
        return self.__next_init_time
    
    @next_init_time.setter
    def next_init_time(self, other: RoutineData):
        self.__next_init_time = other
    
    @property
    def include_this_to_path(self) -> bool:
        return self.__include_this_to_path
    
    @include_this_to_path.setter
    def include_this_to_path(self, other: bool):
        self.__include_this_to_path = bool(other)

#endregion
    
#region IHasEdges
    @property
    def parent(self) -> MinimalistID:
        return self.__parent
    
    @parent.setter
    def parent(self, id: MinimalistID):
        self.__parent = id
    
    @property
    def edges(self) -> list[IMinimalistID]:
        return self.__edges
    
    @edges.setter
    def edges(self, other):
        self.__edges = other
    
    @property
    def raw_edges(self) -> list[IHasEdges]:
        return [self.Nodes.get(id)['value'] for id in self.__edges]
#endregion
    
    def dispose(self) -> None:
        self.Nodes.remove(self.id)
            
        #それぞれのedgeから削除
        for recodes in self.Nodes:
            if isinstance(recodes, EmptyRecode):
                continue
            else:
                node: IHasEdges = recodes['value']
                if self is node:
                    continue

                if node.parent is not None and node.parent == self.id:
                    node.parent = None

                if self.id in node.edges:
                    node.edges.remove(self.id)
                    
    def add_edge(self, other: IHasEdges | IMinimalistID) -> list[IMinimalistID]:
        #idにINodeを入れてしまった場合
        if isinstance(other, IHasEdges):
            return self.add_edge(other.id)
        
        if self.__class__.Nodes.get(other) is EmptyRecode:
            raise ValueError('ノードが存在しません')
        else:
            self.edges.append(other)
            Node.Nodes.get(other)['value'].parent = self.id
            
            return self.edges
    
    def serach(self, search_depth = 100, bfs = True) -> Callable[[Callable], None]:
        """
        Args:
            bfs (bool, optional): Trueなら幅優先探索、Falseなら深さ優先探索を行う
        """
        zero_to_neg = lambda x: -1 if x == False else 0
        popping = lambda list, bfs: Node.Nodes.get(list.pop(bfs))['value']
        
        def __do_serch(func, search_depth=search_depth):
            list: list[MinimalistID] = [self.id]
            
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
    def initialize_tree(self, acquire: Callable[[INodeProperty], tuple[str, str]]) -> None:
        def __next(node: IHasEdges):
            for key, url in acquire(node):
                if key is None or url is None:
                    continue
                else:
                    node.add_edge(Node(key, url, node.tree_height + 1))
        
        self.serach(search_depth=Node.SearchDepth)(__next)
        
    def to_path(self) -> Path:
        if len(Node.Nodes) == 0:
            raise ValueError('ノードが存在しません')
        
        getting: IHasEdges = lambda id: Node.Nodes.get(id)['value']
        
        def loop(id: MinimalistID) -> Path:
            if id is None:
                return Path()
            else:
                node = getting(id)
                return loop(node.parent).joinpath(
                    node.key if node.include_this_to_path else '') #自身を飛ばすかどうか
            
        return loop(self.id)