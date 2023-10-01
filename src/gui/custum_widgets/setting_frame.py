import tkinter as tk
from tkinter import font

from ...data.setting_data import *
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
            if type(w) is InputBox:
                return w
        
class SettingGroup(tk.LabelFrame):
    def __init__(self, master: tk.Misc, key_values: dict, label_title:str=SETTING):
        tk.LabelFrame.__init__(self, master=master, text=label_title)
        
        for key, value_desc in key_values.items():
            value, desc = value_desc.values()
            DescBox(self, key, value, desc)\
                |arrow| (lambda d: d.pack(side=tk.TOP, anchor=tk.W))
            
    @property
    def boxes(self) -> list[InputBox]:
        for w in [b for b in self.winfo_children() if type(b) is DescBox]:
            yield w.box

class SettingFrame(tk.Frame):
    def __init__(self, master: tk.Misc, data: SettingData):
        super().__init__(master=master)
        
        self.__boxes = []
        SettingGroup(self, data.editable_data)\
            |arrow| (lambda g: g.pack(side=tk.LEFT, anchor=tk.NW, padx=(25, 1), pady=4))\
            |arrow| (lambda g: self.__boxes.extend(g.boxes))
        
        label = tk.Label(self)\
            |arrow| (lambda l: l.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5))
            
        tk.Button(self, text=SETTING)\
            |arrow| (lambda b: b.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5))\
            |arrow| (lambda b: b.bind(BUTTON_PRESS, lambda e: self.__save_and_reset_message_show(data.nodes, self.__boxes, label)))        
        
        self.set(self.__boxes, data)
        
    def set(self, targets: list, data: SettingData):
        for data, box in zip(vars(data).values(), targets):
            if box is None:
                continue
            else:
                box.set(data)
        
    def values(self, nodes: list, boxes: list) -> SettingData:
        args = [*map(lambda box: box.value(), filter(lambda box: box is not None, boxes)), nodes]
        return SettingData(*args)
        
    def __save_and_reset_message_show(self, nodes: list, boxes: list, label: tk.Label):
        label[TEXT] = SETTING_RESET_MESSAGE
        file_path = SettingData.SETTINGFOLDER_PATH.joinpath('setting.json')
        save(file_path, self.values(nodes, boxes))