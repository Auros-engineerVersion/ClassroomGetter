import tkinter as tk
from tkinter import ttk
from time import sleep

from ..interface import ISettingData
from ..literals import *
from ..my_util import *
from .custum_widgets import *

class ApplicationRoot(tk.Tk):
    def __init__(self, cfg: ISettingData, size: tuple) -> None:
        super().__init__()
        self.__on_loop_start = identity
        self.__on_loop_end = identity
        
        self.__allow_run = True
        
        self\
            |arrow| (lambda w: w.title(ROOT_TITLE))\
            |arrow| (lambda w: w.geometry(size_to_geometory(*size)))
        
        ttk.Notebook(self, width=size[0], height=size[1])\
            |arrow| (lambda n: n.pack(fill=tk.BOTH, expand=True))\
            |arrow| (lambda n: n.add(text=MAIN,    child=FrontFrame(n, Node.root())))\
            |arrow| (lambda n: n.add(text=SETTING_WINDOW, child=SettingFrame(n, cfg)))
                    
    def run(self, fps: int = 12):
        while self.__allow_run:
            self.__on_loop_start()
            self.update()
            self.update_idletasks()
            self.__on_loop_end()
            sleep(1/fps)
        
    def on_loop_start(self, f, **kwargs):
        """ApplicationRootの一ループの始まりに実行される"""
        self.__on_loop_start = lambda: f(**kwargs)
        
    def on_loop_end(self, f, **kwargs):
        """ApplicationRootの一ループの終わりに実行される"""
        self.__on_loop_end = lambda: f(**kwargs)
        
    def on_stop(self, f, **kwargs):
        """ApplicationRootが終了するときに実行される"""
        #allow_runに代入するためには無名関数では不適である
        #そのため一時的な関数を作成した
        def _temp():
            self.__allow_run = False
            f(**kwargs)
        
        self.protocol(WM_DELETE_WINDOW, _temp)