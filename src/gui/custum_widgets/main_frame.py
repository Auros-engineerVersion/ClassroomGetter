import tkinter as tk

from src.interface.i_node import INode
from src.gui.custum_widgets.base.infomations import *
from src.gui.custum_widgets.base.scrollable_frame import ScrollableFrame

class MainFrame(tk.Frame):
    def __init__(self, master: tk.Misc, root: INode, width: int, height: int):
        tk.Frame.__init__(self, master)
        #アスペクト比を維持したまま小さいサイズにする
        node_canvas = ScrollableFrame(self, tk.SUNKEN, width=width/5, height=height/5, padx=1, pady=1)
        node_info = NodeInfoFrame(self)
        root_box = NodeBox(node_canvas.scrollable_frame, node_info.set_box, root) #最初の頂点を初期化, これは動的にpackされる
        node_info.set_box(root_box)
        
        node_canvas.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)
        node_info.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)