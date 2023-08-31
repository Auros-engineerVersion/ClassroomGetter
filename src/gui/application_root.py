import tkinter as tk
from tkinter import ttk
import asyncio

from .literals import *
from .custum_widgets import * 
from ..data import BrowserControlData as bc_data
from src.setting.settings import Settings, SettingData

class ApplicationRoot(tk.Tk):
    def __init__(self, cfg: SettingData, bc: bc_data, size: tuple) -> None:
        tk.Tk.__init__(self)
        
        self.title(ROOT_TITLE)
        self.geometry(f'{size[0]}x{size[1]}')
        
        note = ttk.Notebook(self, width=size[0], height=size[1])
        main_frame = FrontFrame(note, None if len(cfg.nodes) > 0 else min(cfg.nodes)) #頂点を探して設定する
        setting_frame = SettingFrame(note, cfg)
        
        note.bind(NOTEBOOK_TAB_CHANGED, lambda event: self.resize(note))
        
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
        cfg = Settings.load(SettingData.SETTINGFOLDER_PATH)
        if cfg.is_default():
            cfg.profile = ProfileForm.pop_up('ProfileForm')
        
        bc = bc_data(setting=cfg)
        Settings.setup_data(cfg, bc)

        return (cfg, bc)
        
    async def run_async(self, refresh_rate: int):
        self.__is_running = True
        while self.__is_running:
            self.update()
            await asyncio.sleep(1/refresh_rate)
            
    def stop(self, cfg: SettingData, bc: bc_data):
        del bc
        self.destroy()
        self.__is_running = False