from __future__ import annotations

import gc
import tkinter as tk

from ....literals import *
from ....interface import *
from ....my_util import arrow, identity
from ..base.switch import Switch

class NodeBox(tk.Frame):
    node_info_frame = None
    
    def __init__(self, master: tk.Misc, node: lambda: type('INode', (INodeProperty, IHasEdges)), parent: NodeBox = None):
        tk.Frame.__init__(self, master)
        self.__master = master
        self.__parent_box: NodeBox = parent
        self.__node: INodeProperty = node
        self.__nextboxes: list[NodeBox] = []
        
        self.__on_expand = identity
        self.__on_close = identity
        
        #dropdown
        Switch(master=self, default_state=False, width=self.winfo_height())\
            |arrow| (lambda s: s.pack(side=tk.LEFT))\
            |arrow| (lambda s: s.on_active(self.expand))\
            |arrow| (lambda s: s.on_not_active(self.close))

        #tree_height
        tk.Label(self, text=str(node.tree_height) + ':')\
            |arrow| (lambda b: b.pack(side=tk.LEFT))
        
        #node_key
        tk.Label(self, text=str(node.key))\
            |arrow| (lambda l: l.pack(side=tk.LEFT))
        
        self.pack(anchor=tk.W, padx=(node.tree_height*20, 1), after=self.__parent_box)
    
    @property
    def text(self):
        return self.__node.key
    
    @property
    def url(self):
        return self.__node.url
    
    @property
    def include_this_to_path(self):
        return self.__node.include_this_to_path
    
    @include_this_to_path.setter
    def include_this_to_path(self, other: bool):
        self.__node.include_this_to_path = bool(other)
    
    @property
    def time(self) -> IRoutineData:
        return self.__node.next_init_time
    
    @time.setter
    def time(self, data):
        self.__node.next_init_time = data
        
    def dispose(self):
        stack: list[NodeBox] = [self]
        while(len(stack) > 0):
            value = stack.pop()
            
            for box in value.__nextboxes:
                stack.append(box)

            value.destroy()
        
    def initialize(self, aqcuire):
        self.__node.edges.clear() #子を初期化する
        self.__node.initialize_tree(aqcuire)
        self.close()
                    
    def expand(self):
        self.pack(anchor=tk.W)
        for node in self.__node.raw_edges:
            new_box = NodeBox(self.__master, node, self)
            self.__on_expand(new_box)
            self.__nextboxes.append(new_box)
                
    def close(self):
        #子を初期化する
        for next in self.__nextboxes:
            self.__on_close(next)
            next.dispose()
        self.__nextboxes.clear()
        gc.collect()
        
    def on_click_this(self, f, **kwargs):
        for label in [w for w in self.winfo_children() if isinstance(w, tk.Label)]:
            label.bind(BUTTON_PRESS, lambda _: f(**kwargs))
            
    def on_expand(self, f, **kwargs):
        """渡される関数は新しく生成されたNodeBoxを引数として受け取る"""
        self.__on_expand = lambda n: f(n, **kwargs)
        
    def on_close(self, f, **kwargs):
        """渡される関数は新しく生成されたNodeBoxを引数として受け取る"""
        self.__on_close = lambda: f(**kwargs)