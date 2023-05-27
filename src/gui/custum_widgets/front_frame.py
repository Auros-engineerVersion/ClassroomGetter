import tkinter as tk

from src.interface.i_node import INode
from src.gui.custum_widgets.base.infomations import *
from src.gui.custum_widgets.base.scrollable_frame import ScrollableFrame

class FrontFrame(tk.Frame):
    def __init__(self, master: tk.Misc, root: INode, width: int, height: int):
        tk.Frame.__init__(self, master)
        #アスペクト比を維持したまま小さいサイズにする
        node_canvas = ScrollableFrame(self, tk.SUNKEN, width=width/5, height=height/5, padx=1, pady=1)
        self.__node_info = NodeInfoFrame(self, NodeBox(node_canvas.scrollable_frame, root))
        NodeBox.node_info_frame = self.__node_info
        
        node_canvas.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)
        self.__node_info.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
    async def run_clock(self):
        self.__node_info.run_clock_async()