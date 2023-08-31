import tkinter as tk
from tkinter import font

from ...my_util import size_to_geometory
from ..literals import *
from ...setting import *
from .info_boxes.input_boxes import *

class DescBox(tk.Frame):
    def __init__(self, master: tk.Misc, box: InputBox = ..., text: str = ..., font_size: int = 8):
        tk.Frame.__init__(self, master, relief=tk.GROOVE, bd=1, background=master[BACKGROUND], padx=1, pady=1)
        box.pack(side=tk.TOP, anchor=tk.W)
        self.update_idletasks()

        text_box = tk.Text(self, 
            width=font_size * 4,
            height=2,
            relief=tk.FLAT,
            background=master[BACKGROUND],
            font=(font.nametofont(TK_DEFAULT_FONT), font_size)
        )
        
        text_box.insert(tk.END, text)
        text_box.configure(state='disabled')
        text_box.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, expand=True)
        
class SettingGroup(tk.Frame):
    def __init__(self, master: tk.Misc, values, desc_dic):
        tk.Frame.__init__(self, master, relief=tk.GROOVE, bd=1, background=master[BACKGROUND], padx=5, pady=5)
        
        self.__boxes = []
        for value in values: #変数を取得、それを元にInputBoxを作成、さらにそれに基づくDescBoxを作成
            input_box = box_factory(*value)(self)
            DescBox(self, input_box, desc_dic[value[0]], font_size=8).pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)
            self.__boxes.append(input_box)
            
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
        tk.Frame.__init__(self, master)
        
        self.__boxes = []
        count = 0
        for v in data.normal_data(), data.advanced_data():
            group = SettingGroup(self, values=v, desc_dic=SettingData.DESCRIPTIONS)
            group.pack(side=tk.LEFT, anchor=tk.NW, padx=(1, 25), pady=4)
            self.__boxes.extend(group.boxes)
        
        setting_pop_label = tk.Label(self)
        set_button = tk.Button(self, text=SETTING, command=lambda: self.__save_and_reset_message_show(data.nodes, self.__boxes, setting_pop_label))
        
        setting_pop_label.pack(side=tk.BOTTOM, anchor=tk.E)
        set_button.pack(side=tk.BOTTOM, anchor=tk.E)
        
        self.set(self.__boxes, data)
        
    def resize(self, width: int = 800, height: int = 600):
        root = self.winfo_toplevel()
        root.resizable(width=False, height=False)
        root.geometry(size_to_geometory(width, height))
        
    def set(self, targets: list, data: SettingData):
        data_set = map(
            lambda d, box: box.set(d) if box is not None else None,
            vars(data).values(), targets
        )
        list(data_set)
        
    def values(self, nodes: list, boxes: list) -> SettingData:
        args = [*map(lambda box: box.value(), filter(lambda box: box is not None, boxes)), nodes]
        return SettingData(*args)
        
    def __save_and_reset_message_show(self, nodes: list, boxes: list, label: tk.Label):
        label[TEXT] = SETTING_RESET_MESSAGE
        Settings.save(SettingData.SETTINGFOLDER_PATH, self.values(nodes, boxes))