import tkinter as tk
from tkinter import font

from src.gui.literals import *
from src.my_util import identity
from src.setting.settings import Settings, SettingData
from src.gui.custum_widgets.info_boxes.input_boxes import box_factory, InputBox

class DescBox(tk.Frame):
    def __init__(self, master: tk.Misc, box: InputBox, text: str, font_size: int):
        tk.Frame.__init__(self, master, relief=tk.GROOVE, background=master[BACKGROUND], padx=5, pady=5)
        box.pack(side=tk.TOP, anchor=tk.W)
        self.update_idletasks()

        text_box = tk.Text(self, 
            width=box.winfo_reqwidth(),
            height=1,
            relief=tk.FLAT,
            background=master[BACKGROUND],
            font=(font.nametofont(TK_DEFAULT_FONT), font_size)
        )
        
        text_box.insert(tk.END, text)
        text_box.configure(state='disabled')
        text_box.pack(side=tk.LEFT, anchor=tk.W)

class SettingFrame(tk.Frame):
    def __init__(self, master: tk.Misc, data: SettingData):
        tk.Frame.__init__(self, master)
        
        self.__boxes = []        
        box_create = map(
            lambda box, text: DescBox(self, box, text, font_size=8) if box is not None else None,
            map(
                lambda args: identity(box_factory(*args)(self))(self.__boxes.append),
                vars(data).items()
            ),
            SettingData.DESCRIPTIONS.values()
        )

        box_set = map(
            lambda box: box.pack(side=tk.TOP, anchor=tk.W) if box is not None else None,
            box_create
        )
        list(box_set)
        
        setting_pop_label = tk.Label(self)
        set_button = tk.Button(self, text=SETTING, command=lambda: self.__save_and_reset_message_show(data.nodes, self.__boxes, setting_pop_label))
        
        setting_pop_label.pack(side=tk.BOTTOM, anchor=tk.E)
        set_button.pack(side=tk.BOTTOM, anchor=tk.E)
        
        self.set(self.__boxes, data)
        
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