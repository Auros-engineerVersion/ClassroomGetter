import tkinter as tk
from tkinter import ttk
import asyncio

from src.gui.custum_widgets.info_boxes.input_boxes import *
from gui.custum_widgets.front_frame import FrontFrame
from src.gui.custum_widgets.setting_frame import SettingFrame
from src.setting.settings import Settings, SettingData
from src.data.nodes import Node
from src.browser.browser_controls import BrowserControl

class Window(tk.Frame):
    @staticmethod
    def setup():
        cfg = Settings.load(SettingData.SETTINGFOLDER_PATH)
        if cfg.is_default():
            prof = Window.InputForm()
            cfg.user_email = prof[0]
            cfg.user_password = prof[1]
        
        bc = BrowserControl(setting=cfg)
        Node.BrowserControl = bc
        Settings.setup_data(cfg, bc)

        return cfg
    
    @staticmethod
    def __size(width: int, height: int) -> str:
        return str(width) + 'x' + str(height)

    @staticmethod
    def InputForm(master: tk.Misc = None) -> tuple:
        if master == None:
            master = tk.Tk()
        
        master.title('Form')
        master.resizable(0, 0) #windowのサイズ変更を許可しない
        
        padx_size = (5, 10)
        width = 30
        
        email    = EntryInput(master, width=width, padx=padx_size, title='email')
        password = EntryInput(master, width=width, padx=padx_size, title='password')
        complete_button = tk.Button(master, text='完了', command=master.quit)

        # ウィジェットの配置
        email.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        password.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        complete_button.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5)
        
        master.mainloop()
                
        #入力された値を取得して返す
        email_info     = str(email.value())
        password_info  = str(password.value())
        master.destroy() #値を取得できたらフォームを解放する
        return (email_info, password_info)