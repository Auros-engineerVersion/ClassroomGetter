from __future__ import annotations
import gc
import tkinter as tk
from typing import Callable

from src.interface.i_node import INode

RUN = '実行'
LOADING = '更新中'
BUTTON_PRESS = "<ButtonPress>"
TEXT = "text"

class NodeBox(tk.Frame):
    def __init__(self, master: tk.Misc, set_info_func: Callable[[NodeBox], None], node: INode, parent: NodeBox = None):
        tk.Frame.__init__(self, master)
        self.__master = master
        self.__set_info_func = set_info_func
        self.__parent_box = parent
        self.__node = node
        self.__is_expand: bool = False
        self.__nextboxes: list[NodeBox] = []
        
        drop_button = tk.Button(self, command=self.expand, width=self.winfo_height())
        height_label = tk.Label(self, text=str(node.tree_height) + ':')
        key_label = tk.Label(self, text=str(node.key))
        
        drop_button.pack(side=tk.LEFT)
        height_label.pack(side=tk.LEFT)
        key_label.pack(side=tk.LEFT)
        
        height_label.bind(BUTTON_PRESS, self.on_frame_click)        
        key_label.bind(BUTTON_PRESS, self.on_frame_click)
        
        self.pack(anchor=tk.W, padx=(node.tree_height*20, 1), after=self.__parent_box)
        
        self.text = key_label[TEXT]
        self.url = node.url
    
    def on_frame_click(self, event):
        self.__set_info_func(self)
        
    def dispose(self):
        stack: list[NodeBox] = [self]
        while(len(stack) > 0):
            value = stack.pop()
            
            for box in value.__nextboxes:
                stack.append(box)

            value.destroy()
        
    def initialize_node(self):
        self.__node.edges().clear()
        self.__node.initialize_tree()
        self.__is_expand = False
                    
    def expand(self):
        #反転する
        self.__is_expand = not self.__is_expand
        
        #子を初期化する
        for next in self.__nextboxes:
            next.dispose()
        self.__nextboxes.clear()
        gc.collect()
        
        if self.__is_expand:
            self.pack(anchor=tk.W)
            for node in self.__node.edges():
                new_box = NodeBox(self.__master, self.__set_info_func, node, self)
                self.__nextboxes.append(new_box)