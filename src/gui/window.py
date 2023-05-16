import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from gui.custum_widgets import custum_widgets as mytk
from src.my_util import identity, tail_recursion
from src.interface.i_node import INode
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
        
        email    = mytk.InputBox(master, width=width, padx=padx_size, title='email')
        password = mytk.InputBox(master, width=width, padx=padx_size, title='password')
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
            
    @staticmethod
    @tail_recursion
    def RunWindow(root_node, cfg, master: tk.Misc = None, width: int = 600, height: int = 300):
        if master is None:
            master = tk.Tk()

        master.title('ClassroomHack')
        master.geometry(Window.__size(width, height))
        master.resizable(0, 0) #windowのサイズ変更を許可しない

        note = ttk.Notebook(master, width=width, height=height)
        main_frame = MainFrame(note, root_node, width, height)
        setting_frame = SettingFrame(note, cfg, width, height)

        note.add(main_frame, text='メイン')
        note.add(setting_frame, text='設定')
        note.pack(expand=True)

        master.mainloop()
        
        return cfg