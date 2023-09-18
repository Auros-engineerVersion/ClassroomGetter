import tkinter as tk
from tkinter import font

from ...data.setting_data import *
from ...literals import *
from ...my_util import *
from ...setting import *
from .info_boxes.input_boxes import *
from .base import *


class DescBox(tk.Frame):
    def __init__(self, master: tk.Misc, box: InputBox = ..., text: str = ..., font_size: int = 8):
        tk.Frame.__init__(self, master, relief=tk.GROOVE, bd=1, background=master[BACKGROUND], padx=1, pady=1)
        box.pack(side=tk.TOP, anchor=tk.W)
        self.update_idletasks()

        #説明文
        tk.Text(self, width=font_size * 4, height=2, relief=tk.FLAT, background=master[BACKGROUND], font=(font.nametofont(TK_DEFAULT_FONT), font_size))\
            |arrow| (lambda t: t.insert(tk.END, text))\
            |arrow| (lambda t: t.configure(state='disabled'))\
            |arrow| (lambda t: t.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, expand=True))
        
class SettingGroup(tk.Frame):
    def __init__(self, master: tk.Misc, key_commentobj):
        tk.Frame.__init__(self, master, relief=tk.GROOVE, bd=1, background=master[BACKGROUND], padx=5, pady=5)
        
        self.__boxes = []
        for key, commentobj in key_commentobj:
            input_box = box_factory(key, commentobj.value)(self)\
                |arrow| (lambda b: b.set(commentobj.value))\
                |arrow| (lambda b: self.__boxes.append(b))
                            
            DescBox(self, input_box, commentobj.comment, font_size=8)\
                .pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)
            
    @property
    def boxes(self) -> list[InputBox]:
        descs = []
        #子のDescBoxを取得
        for box in self.winfo_children():
            if type(box) is DescBox:
                descs.append(box)
                
        result = []
        #DescBoxの子のInputBoxを取得
        for desc in descs:
            for box in desc.winfo_children():
                if type(box) is InputBox:
                    result.append(box)
        
        return result

class SettingFrame(tk.Frame):
    def __init__(self, master: tk.Misc, data: SettingData):
        super().__init__(master=master)
        
        self.__boxes = []
        SettingGroup(self, data.editable_data.items())\
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
        save(SettingData.SETTINGFOLDER_PATH, self.values(nodes, boxes))