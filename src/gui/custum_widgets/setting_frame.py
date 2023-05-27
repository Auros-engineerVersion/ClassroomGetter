import tkinter as tk
from src.my_util import identity
from src.setting.settings import Settings, SettingData
from src.gui.custum_widgets.info_boxes.input_boxes import box_factory

class SettingFrame(tk.Frame):
    def __init__(self, master: tk.Misc, data: SettingData, width: int, height: int):
        tk.Frame.__init__(self, master)
        
        self.__boxes = []        
        box_set = map(
            lambda box: box.pack(side=tk.TOP, anchor=tk.W, fill=tk.X) if box is not None else None,
            map(
                lambda args: identity(box_factory(*args, width)(self))(self.__boxes.append),
                vars(data).items()
            )
        )
        list(box_set)
        
        set_button = tk.Button(self, text='設定', command=lambda: self.save(data.nodes, self.__boxes))
        set_button.pack(side=tk.BOTTOM, anchor=tk.E)
        
        self.set(data)
        
    def set(self, data: SettingData):
        data_set = map(
            lambda d, box: box.set(d) if box is not None else None,
            vars(data).values(), self.__boxes
        )
        list(data_set)
        
    def save(self, nodes: list, boxes: list):
        args = [*map(lambda box: box.value(), filter(lambda box: box is not None, boxes)), nodes]
        data = SettingData(*args)
        Settings.save(SettingData.SETTINGFOLDER_PATH, data)