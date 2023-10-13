import tkinter as tk
from tkinter import font

from ...data import *
from ...literals import *
from ...my_util import *
from ...my_io import *
from .info_boxes.input_boxes import *
from .base import *


class DescBox(tk.Frame):
    def __init__(self, master: tk.Misc, key: str, value: str, description: str, font_size: int = 10):
        super().__init__(master=master)
        self.update_idletasks()
        
        box_factory(self, key, value)\
            |arrow| (lambda b: b.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=True))
            
        #説明文
        tk.Text(self, width=font_size * 4, height=5, relief=tk.FLAT, font=(font.nametofont(TK_DEFAULT_FONT), font_size), background=master[BACKGROUND])\
            |arrow| (lambda t: t.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=True))\
            |arrow| (lambda t: t.insert(tk.END, description))\
            |arrow| (lambda t: t.configure(state='disabled'))
            
    @property
    def box(self) -> InputBox:
        for w in self.winfo_children():
            if isinstance(w, InputBox):
                return w
        
#TODO cfgの変更を反映させる
class SettingGroup(tk.LabelFrame):
    def __init__(self, master: tk.Misc, label_title:str, key_values: dict):
        tk.LabelFrame.__init__(self, master=master, text=label_title)
        
        for key, value_desc in key_values.items():
            value, desc = value_desc.values()
            DescBox(self, key, value, desc)\
                |arrow| (lambda d: d.pack(side=tk.TOP, anchor=tk.W, pady=10))
            
    @property
    def values(self) -> list:
        v = []
        for input_box in [w.box for w in [b for b in self.winfo_children() if isinstance(b, DescBox)]]:
           v.append(input_box.get())
        return v

class SettingFrame(tk.Frame):
    def __init__(self, master: tk.Misc, cfg: ISettingData):
        super().__init__(master=master)
        self.__cfg = cfg
        self.__groups: list[SettingGroup] = []
        
        for data in (self.__cfg.normal, self.__cfg.advanced):
            SettingGroup(self, *data)\
                |arrow| (lambda g: g.pack(side=tk.LEFT, anchor=tk.N, expand=True, fill=tk.BOTH, padx=5, pady=5))\
                |arrow| (lambda g: self.__groups.append(g))
        
        #セーブボタン
        self.__save_btn = tk.Button(self, text=SAVE)\
            |arrow| (lambda b: b.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5))
    
    def current_cfg(self) -> ISettingData:
        args = [group.values for group in self.__groups]
        return SettingData(*args, nodes=Node.Nodes)
    
    def on_save(self, f, **kwargs):
        self.__save_btn.bind(BUTTON_PRESS, lambda _: f(**kwargs))