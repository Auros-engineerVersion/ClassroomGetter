import tkinter as tk

from ...interface import INodeProperty
from ...my_util import arrow
from .base import *


class FrontFrame(tk.Frame):
    def __init__(self, master: tk.Misc, root: INodeProperty = None):
        super().__init__(master=master)
        
        #Node描写用のFrame
        node_canvas = ScrollableFrame(self, tk.SUNKEN, padx=1, pady=1)\
            |arrow| (lambda x: x.pack(side=tk.LEFT, fill=tk.BOTH, expand=True))
            
        self.__node_info = NodeInfoFrame(self, NodeBox(node_canvas.scrollable_frame, root))\
            |arrow| (lambda x: x.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True))
            
        NodeBox.node_info_frame = self.__node_info