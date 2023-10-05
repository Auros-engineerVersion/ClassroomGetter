import tkinter as tk
from tkinter import messagebox, ttk

from ..data import BrowserControlData as bc_data
from ..data import SearchParameterContainer as spc
from ..interface import ISettingData
from ..literals import *
from ..my_util import *
from .custum_widgets import *

def setup_profile(cfg: ISettingData, warning = identity):
    if cfg.is_current_user() or cfg.is_guest():
        return cfg
    else:
        warning()
        cfg.profile = ProfileForm().pop_up()
        return setup_profile(cfg, lambda: messagebox.showwarning(title=WARNING, message=PROFILE_WARNING))

def set_env(cfg: ISettingData):
    spc.browser_control_data = (bc := bc_data(cfg))
    spc.save_dir = cfg.save_folder_path[VALUE]
    
    if not cfg.is_guest():
        classroom_login(bc, *cfg.profile)
        
    return cfg

class ApplicationRoot(tk.Tk):
    def __init__(self, cfg: ISettingData, size: tuple) -> None:
        cfg = set_env(setup_profile(cfg))
        
        tk.Tk.__init__(self)
        self\
            |arrow| (lambda w: w.title(ROOT_TITLE))\
            |arrow| (lambda w: w.geometry(size_to_geometory(*size)))\
            |arrow| (lambda w: w.protocol(WM_DELETE_WINDOW, self.stop))
        
        ttk.Notebook(self, width=size[0], height=size[1])\
            |arrow| (lambda n: n.pack(fill=tk.BOTH, expand=True))\
            |arrow| (lambda n: n.add(text=MAIN,    child=FrontFrame(n, Node.root())))\
            |arrow| (lambda n: n.add(text=SETTING, child=SettingFrame(n, cfg)))
                    
    def stop(self):
        del spc.browser_control_data
        self.destroy()