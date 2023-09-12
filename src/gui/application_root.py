import tkinter as tk
from tkinter import ttk

from .literals import *
from .custum_widgets import * 
from ..data import BrowserControlData as bc_data
from ..setting import *

class ApplicationRoot(tk.Tk):
    def __init__(self, cfg: SettingData, bc: bc_data, size: tuple) -> None:
        tk.Tk.__init__(self)
        
        self.title(ROOT_TITLE)
        self.geometry(f'{size[0]}x{size[1]}')
        
        note = ttk.Notebook(self, width=size[0], height=size[1])
        main_frame = FrontFrame(note, min(cfg.nodes) if len(cfg.nodes) > 0 else None) #頂点を探して設定する
        setting_frame = SettingFrame(note, cfg)
        
        note.bind(NOTEBOOK_TAB_CHANGED, lambda e: self.resize(note))
        
        self.__cfg = cfg #状態を持たせるために必要
        self.protocol(WM_DELETE_WINDOW, lambda: self.stop(self.__cfg, bc))

#region pack
        note.add(main_frame, text=MAIN)
        note.add(setting_frame, text=SETTING)
        note.pack(fill=tk.BOTH, expand=True)
#endregion
        
    #NoteBookを引数にとる。そのNoteBoolのページが遷移した際、windowのサイズを変更する関数
    def resize(self, note: ttk.Notebook):
        note.nametowidget(note.select()).resize()
        
    @staticmethod
    def setup() -> tuple[SettingData, bc_data]:
        cfg = load(SettingData.SETTINGFOLDER_PATH)
        if cfg.is_default():
            cfg.profile = ProfileForm.pop_up('ProfileForm')

        bc = bc_data(setting=cfg)
        return setup_data(cfg, bc)
            
    def stop(self, cfg: SettingData, bc: bc_data):
        del bc
        self.destroy()