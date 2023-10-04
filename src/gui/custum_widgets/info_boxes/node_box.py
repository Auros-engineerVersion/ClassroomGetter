from __future__ import annotations

import gc
import tkinter as tk

from ....literals import *
from ....interface import INodeProperty, IHasEdges
from ....my_util import arrow
from ..base.switch import Switch

class NodeBox(tk.Frame):
    node_info_frame = None
    
    def __init__(self, master: tk.Misc, node: lambda: type('INode', (INodeProperty, IHasEdges)), parent: NodeBox = None):
        tk.Frame.__init__(self, master)
        self.__master = master
        self.__parent_box = parent
        self.__node = node
        self.__nextboxes: list[NodeBox] = []
        
        #dropdown
        Switch(master=self, default_state=False, width=self.winfo_height())\
            |arrow| (lambda s: s.on_active(self.expand))\
            |arrow| (lambda s: s.on_not_active(self.close))\
            |arrow| (lambda s: s.pack(side=tk.LEFT))

        #tree_height
        tk.Label(self, text=str(node.tree_height) + ':')\
            |arrow| (lambda b: b.bind(BUTTON_PRESS, self.on_frame_click))\
            |arrow| (lambda b: b.pack(side=tk.LEFT))
        
        #node_key
        tk.Label(self, text=str(node.key))\
            |arrow| (lambda l: l.bind(BUTTON_PRESS, self.on_frame_click))\
            |arrow| (lambda l: l.pack(side=tk.LEFT))
        
        self.pack(anchor=tk.W, padx=(node.tree_height*20, 1), after=self.__parent_box)
        
    @property
    def time(self):
        return self.__node.next_init_time
    
    @property
    def text(self):
        return self.__node.key
    
    @property
    def url(self):
        return self.__node.url
    
    def set_time(self, data):
        self.__node.next_init_time = data
            
    def time_reset(self, event):
        self.__node.next_init_time.reset()
    
    def on_frame_click(self, event):
        NodeBox.node_info_frame.set_box(self)
        
    def dispose(self):
        stack: list[NodeBox] = [self]
        while(len(stack) > 0):
            value = stack.pop()
            
            for box in value.__nextboxes:
                stack.append(box)

            value.destroy()
        
    def initialize(self):
        self.__node.edges.clear() #子を初期化する
        self.__node.initialize_tree()
                    
    def expand(self):
        self.pack(anchor=tk.W)
        for node in self.__node.raw_edges:
            new_box = NodeBox(self.__master, node, self)
            self.__nextboxes.append(new_box)
                
    def close(self):
        #子を初期化する
        for next in self.__nextboxes:
            next.dispose()
        self.__nextboxes.clear()
        gc.collect()