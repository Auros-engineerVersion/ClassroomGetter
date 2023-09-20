import tkinter as tk
from tkinter import messagebox, ttk

from ..data import BrowserControlData as bc_data
from ..data import SearchParameterContainer as spc
from ..interface import ISettingData
from ..literals import *
from ..my_util import identity, pipe
from .custum_widgets import FrontFrame, SettingFrame
from .custum_widgets.info_boxes import ProfileForm


class ApplicationRoot(tk.Tk):
    def __init__(self, cfg: ISettingData, size: tuple) -> None:
        cfg = self.__set_spc(self.__setup_profile(cfg))
        
        tk.Tk.__init__(self)
        
        self.title(ROOT_TITLE)
        self.geometry(f'{size[0]}x{size[1]}')
        
        note = ttk.Notebook(self, width=size[0], height=size[1])
        main_frame = FrontFrame(note, min(cfg.nodes)) #頂点を探して設定する
        setting_frame = SettingFrame(note, cfg)
                
        self.protocol(WM_DELETE_WINDOW, self.stop)

#region pack
        note.add(main_frame, text=MAIN)
        note.add(setting_frame, text=SETTING)
        note.pack(fill=tk.BOTH, expand=True)
#endregion

    def __setup_profile(self, cfg: ISettingData, warning = lambda: identity(1)):
        if cfg.is_current_user() or cfg.is_guest():
            return cfg
        else:
            warning()
            cfg.profile = ProfileForm().pop_up()
            return self.__setup_profile(cfg, lambda: messagebox.showwarning(title=WARNING, message=PROFILE_WARNING))
    
    def __set_spc(self, cfg: ISettingData):
        spc.browser_control_data = bc_data(cfg)
        return cfg
        
    def stop(self):
        del spc.browser_control_data
        self.destroy()