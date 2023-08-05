import tkinter as tk

from src.gui.literals import CONFIGURE
from src.my_util import size_to_geometory
from src.interface.i_node import INode
from src.gui.custum_widgets.base.infomations import *
from src.gui.custum_widgets.base.scrollable_frame import ScrollableFrame

class FrontFrame(tk.Frame):
    def __init__(self, master: tk.Misc, root: INode = None):
        tk.Frame.__init__(self, master)
        node_canvas = ScrollableFrame(self, tk.SUNKEN, padx=1, pady=1)
        self.__node_info = NodeInfoFrame(self, NodeBox(node_canvas.scrollable_frame, root))
        NodeBox.node_info_frame = self.__node_info
        
        node_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.__node_info.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def resize(self, width: int = 400, height: int = 300):
        root = self.winfo_toplevel()
        root.resizable(True, True)
        root.geometry(size_to_geometory(width, height))
        
    async def run_clock(self):
        self.__node_info.run_clock_async()