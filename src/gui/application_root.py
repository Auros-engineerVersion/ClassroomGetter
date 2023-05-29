import tkinter as tk
from tkinter import ttk
import asyncio

from src.gui.custum_widgets.front_frame import *
from src.gui.custum_widgets.setting_frame import *
from src.data.browser_control_data import BrowserControlData as bc_data
from src.gui.custum_widgets.info_boxes.input_boxes import ProfileForm
from src.setting.settings import Settings, SettingData

ROOT_TITLE = 'ClassroomHack'
WM_DELETE_WINDOW = 'WM_DELETE_WINDOW'

class ApplicationRoot(tk.Tk):
    def __init__(self, cfg: SettingData, bc: bc_data, size: tuple) -> None:
        tk.Tk.__init__(self, sync=True)
        
        self.title = ROOT_TITLE
        self.geometry(f'{size[0]}x{size[1]}')
        self.resizable(0, 0)
                
        note = ttk.Notebook(self, width=size[0], height=size[1])
        main_frame = FrontFrame(note, min(cfg.nodes), *size) #頂点を探して設定する
        setting_frame = SettingFrame(note, cfg, *size)
        
        self.__cfg = cfg #状態を持たせるために必要
        self.protocol(WM_DELETE_WINDOW, lambda: self.stop(self.__cfg, bc))

#region pack
        note.add(main_frame, text='メイン')
        note.add(setting_frame, text='設定')
        note.pack(expand=True)
#endregion
        
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
        Settings.save(cfg.SETTINGFOLDER_PATH, cfg)
        del bc
        self.destroy()
        self.__is_running = False