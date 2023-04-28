import tkinter as tk
from tkinter import ttk

from src.gui import custum_widgets as mytk

class Window(tk.Frame):
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
        email_info     = email.value()
        password_info  = password.value()
        master.destroy() #値を取得できたらフォームを解放する
        return (email_info, password_info)
            
    @staticmethod
    def RunWindow(root_node, cfg, master: tk.Misc = None, width: int = 600, height: int = 300):        
        if master is None:
            master = tk.Tk()
        
        master.title('ClassroomHack')
        master.geometry(Window.__size(width, height))
        master.resizable(0, 0) #windowのサイズ変更を許可しない
    
        note = ttk.Notebook(master, width=width, height=height)
        main_frame = mytk.MainFrame(note, root_node, width, height)
        setting_frame = mytk.SettingFrame(note, cfg, width, height)
        
        note.add(main_frame, text='メイン')
        note.add(setting_frame, text='設定')
        
        note.pack(expand=True)

        master.mainloop()