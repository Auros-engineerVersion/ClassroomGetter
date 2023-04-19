from __future__ import annotations
import gc
import tkinter as tk
from src.interface.i_node import INode
from src.setting.setting_data import SettingData

BUTTON_PRESS = "<ButtonPress>"

class ScrollableFrame(tk.Frame):
    def __init__(self, master: tk.Misc, relief: str, width: int, height: int, padx: int, pady: int, bar_x = True, bar_y = True):
        tk.Frame.__init__(self, master, width=width, height=height, padx=padx, pady=pady, background='red')
        self.canvas = tk.Canvas(self, relief=relief, borderwidth=1)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox(tk.ALL)
            )
        )
                
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        if bar_y:
            self.scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        if bar_x:
            self.scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
            self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
            
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

class InputBox(tk.Frame):
    def __init__(self, master: tk.Misc, width: int = 30, padx: tuple = (1, 1), title: str = 'title'):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text=title)
        t_box = tk.Entry(self, width=width)
        
        label.pack(side=tk.LEFT, anchor=tk.W, ipadx=1, padx=padx)
        t_box.pack(side=tk.RIGHT, anchor=tk.E, ipadx= 1, padx=padx[:-1]) #tupleを反転させる
            
class NodeBox(tk.Frame):
    node_info_box: NodeInfoFrame = None
    def __init__(self, master: tk.Misc, node: INode, parent: NodeBox = None):
        tk.Frame.__init__(self, master)
        drop_button = tk.Button(self, command=self.expand, width=self.winfo_height())
        height_label = tk.Label(self, text=str(node.tree_height) + ':')
        key_label = tk.Label(self, text=str(node.key))
        url_label = tk.Label(self, text=str(node.url))
        
        drop_button.pack(side=tk.LEFT)
        height_label.pack(side=tk.LEFT)
        key_label.pack(side=tk.LEFT)
        url_label.pack(side=tk.LEFT)
        
        height_label.bind(BUTTON_PRESS, self.on_frame_click)        
        key_label.bind(BUTTON_PRESS, self.on_frame_click)
        url_label.bind(BUTTON_PRESS, self.on_frame_click)
                
        self.node = node
        self.is_expand: bool = False
        self.__master = master
        self.__parent_box = parent
        self.__nextboxes: list[NodeBox] = []
        
        self.pack(anchor=tk.W, padx=(node.tree_height*20, 1), after=self.__parent_box)

    def on_frame_click(self, event):
        self.node_info_box.update_text(self)

    def dispose(self):
        stack: list[NodeBox] = [self]
        
        while(len(stack) > 0):
            value = stack.pop()
            
            for box in value.__nextboxes:
                stack.append(box)

            value.destroy()
                    
    def expand(self):
        #反転する
        self.is_expand = not self.is_expand
        
        #子を初期化する
        for next in self.__nextboxes:
            next.dispose()
        self.__nextboxes.clear()
        gc.collect()
        
        if self.is_expand:
            self.pack(anchor=tk.W)
            for node in self.node.edges():
                self.__nextboxes.append(NodeBox(self.__master, node, self))

            
class NodeInfoFrame(tk.Frame):
    def __init__(self, master: tk.Misc, watching_box: NodeBox = None):
        tk.Frame.__init__(self, master, background='green')
        
        self.__watching_box = watching_box
        self.__node_name_label = tk.Label(self, text=watching_box.node.key if watching_box.node != None else 'No Data')
        #ボタンが押されたら、監視中のNodeからinitialize_treeを実行する
        initialize_button = tk.Button(self, text='実行', 
            command=lambda: self.do_initialize_tree(self.__watching_box))
        
        self.__node_name_label.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=5)
        initialize_button.pack(side=tk.BOTTOM, fill=tk.X)
        
    def update_text(self, target_box: NodeBox):
        self.__watching_box = target_box
        self.__node_name_label['text'] = target_box.node.key
        
    @staticmethod
    def do_initialize_tree(box: NodeBox):
        #子を初期化する
        box.node.edges().clear()
        box.node.initialize_tree(box.node)
        box.is_expand = False