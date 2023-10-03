import tkinter as tk
from tkinter import font

from ...data import *
from ...literals import *
from ...my_util import *
from ...settings import *
from .info_boxes.input_boxes import *
from .base import *


class DescBox(tk.Frame):
    def __init__(self, master: tk.Misc, key: str, value: str, description: str, font_size: int = 10):
        super().__init__(master=master)
        self.update_idletasks()
        
        box_factory(self, key, value)\
            |arrow| (lambda b: b.pack(side=tk.TOP))
            
        #説明文
        tk.Text(self, width=font_size * 4, height=2, relief=tk.FLAT, font=(font.nametofont(TK_DEFAULT_FONT), font_size), background=master[BACKGROUND])\
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
    def __init__(self, master: tk.Misc, key_values: dict, label_title:str=SETTING):
        tk.LabelFrame.__init__(self, master=master, text=label_title)
        
        for key, value_desc in key_values.items():
            value, desc = value_desc.values()
            DescBox(self, key, value, desc)\
                |arrow| (lambda d: d.pack(side=tk.TOP, anchor=tk.W))
            
    @property
    def boxes(self) -> list[InputBox]:
        for w in [b for b in self.winfo_children() if isinstance(b, DescBox)]:
            yield w.box

class SettingFrame(tk.Frame):
    def __init__(self, master: tk.Misc, cfg: ISettingData):
        super().__init__(master=master)
        self.__cfg = cfg
        
        self.groups: SettingGroup = SettingGroup(self, self.__cfg.editable_data)\
            |arrow| (lambda g: g.pack(side=tk.LEFT, anchor=tk.NW, padx=(25, 1), pady=4))\
            
        tk.Button(self, text=SAVE)\
            |arrow| (lambda b: b.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5))\
            |arrow| (lambda b: b.bind(BUTTON_PRESS, 
                    self.__save_cfg(cfg.SETTINGFOLDER_PATH.joinpath('setting.json'))))
            
    def __save_cfg(self, file_path: Path):
        def _inner(e):
            values = [box.get() for box in self.groups.boxes]
            try_save(file_path, SettingData(*values, nodes=self.__cfg.nodes))
        return _inner