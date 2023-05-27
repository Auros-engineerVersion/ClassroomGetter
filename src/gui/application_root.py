import tkinter as tk
from tkinter import ttk
import asyncio

from src.gui.custum_widgets.front_frame import *
from src.gui.custum_widgets.setting_frame import *
from src.gui.custum_widgets.info_boxes.input_boxes import ProfileForm
from src.data.browser_control_data import BrowserControlData as bc_data
from src.setting.settings import Settings, SettingData

ROOT_TITLE = 'ClassroomHack'
WM_DELETE_WINDOW = 'WM_DELETE_WINDOW'

class ApplicationRoot(tk.Tk):
    def __init__(self, root_node, cfg, size: tuple) -> None:
        tk.Tk.__init__(self)
        
        self.title = ROOT_TITLE
        self.geometry(f'{size[0]}x{size[1]}')
        self.resizable(0, 0)
        
        note = ttk.Notebook(self, width=self.winfo_width(), height=self.winfo_height())
        main_frame = FrontFrame(note, root_node, self.winfo_width(), self.winfo_height())
        setting_frame = SettingFrame(note, cfg, self.winfo_width(), self.winfo_height())
        
        self.__cfg = cfg
        self.protocol(WM_DELETE_WINDOW, lambda: self.stop(self.__cfg))

#region pack
        note.add(main_frame, text='メイン')
        note.add(setting_frame, text='設定')
        note.pack(expand=True)
#endregion
        
    @staticmethod
    def setup():
        cfg = Settings.load(SettingData.SETTINGFOLDER_PATH)
        if cfg.is_default():
            cfg.profile = ProfileForm.pop_up('ProfileForm')
        
        Settings.setup_data(cfg, bc_data(setting=cfg))

        return cfg
        
    async def run_async(self, refresh_rate: int):
        while True:
            self.update()
            await asyncio.sleep(1/refresh_rate)
            
    def stop(self, cfg: SettingData):
        Settings.save(cfg.SETTINGFOLDER_PATH, cfg)
        self.destroy()