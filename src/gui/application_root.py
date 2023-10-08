import tkinter as tk
from tkinter import ttk

from ..interface import ISettingData
from ..literals import *
from ..my_util import *
from .custum_widgets import *

class ApplicationRoot(tk.Tk):
    def __init__(self, cfg: ISettingData, size: tuple) -> None:
        super().__init__()
        self.__on_loop_start = identity
        self.__on_loop_end = identity
        
        self\
            |arrow| (lambda w: w.title(ROOT_TITLE))\
            |arrow| (lambda w: w.geometry(size_to_geometory(*size)))\
            |arrow| (lambda w: w.protocol(WM_DELETE_WINDOW, self.stop))
        
        ttk.Notebook(self, width=size[0], height=size[1])\
            |arrow| (lambda n: n.pack(fill=tk.BOTH, expand=True))\
            |arrow| (lambda n: n.add(text=MAIN,    child=FrontFrame(n, Node.root())))\
            |arrow| (lambda n: n.add(text=SETTING, child=SettingFrame(n, cfg)))
            
    def __del__(self):
        self.stop()
                    
    def run(self):
        while True:
            self.__on_loop_start()
            self.update()
            self.update_idletasks()
            self.__on_loop_end()
                    
    def stop(self):
        self.destroy()
        
    def on_loop_start(self, f, **kwargs):
        """ApplicationRootの一ループの始まりに実行される"""
        self.__on_loop_start = lambda: f(**kwargs)
        
    def on_loop_end(self, f, **kwargs):
        """ApplicationRootの一ループの終わりに実行される"""
        self.__on_loop_end = lambda: f(**kwargs)