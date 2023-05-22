import tkinter as tk
from tkinter import ttk

from src.gui.custum_widgets.front_frame import *
from src.gui.custum_widgets.setting_frame import *

ROOT_TITLE = 'ClassroomHack'

class ApplicationRoot(tk.Tk):
    def __init__(self, root_node, cfg, size: tuple) -> None:
        tk.Tk.__init__(self)
        
        self.title = ROOT_TITLE
        self.geometry(f'{size[0]}x{size[1]}')
        self.resizable(0, 0)
        
        note = ttk.Notebook(self, width=self.winfo_width(), height=self.winfo_height())
        main_frame = FrontFrame(note, root_node, self.winfo_width(), self.winfo_height())
        setting_frame = SettingFrame(note, cfg, self.winfo_width(), self.winfo_height())

        note.add(main_frame, text='メイン')
        note.add(setting_frame, text='設定')
        note.pack(expand=True)