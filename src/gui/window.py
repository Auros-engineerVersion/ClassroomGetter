import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from src.gui import custum_widgets as mytk
from src.my_util import identity, tail_recursion, Jump
from src.interface.i_node import INode
from src.setting.settings import Settings, SettingData
import src.data.setting_data
from src.data.nodes import Node
from src.browser.browser_controls import BrowserControl

class MainFrame(tk.Frame):
    def __init__(self, master: tk.Misc, root: INode, width: int, height: int):
        tk.Frame.__init__(self, master)
        #アスペクト比を維持したまま小さいサイズにする
        node_canvas = mytk.ScrollableFrame(self, tk.SUNKEN, width=width/5, height=height/5, padx=1, pady=1)
        node_info = mytk.NodeInfoFrame(self)
        root_box = mytk.NodeBox(node_canvas.scrollable_frame, node_info, root) #最初の頂点を初期化, これは動的にpackされる
        node_info.set_box(root_box)
        
        node_canvas.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)
        node_info.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
class SettingFrame(tk.Frame):
    def __init__(self, master: tk.Misc, data: SettingData, width: int, height: int):
        tk.Frame.__init__(self, master)
        
        self.__boxes = []        
        box_set = map(
            lambda box: box.pack(side=tk.TOP, anchor=tk.W, fill=tk.X) if box is not None else None,
            map(
                lambda args: identity(mytk.box_factory(*args, width)(self))(self.__boxes.append),
                vars(data).items()
            )
        )
        list(box_set)
        
        set_button = tk.Button(self, text='設定', command=lambda: self.save(data.node_list, self.__boxes))
        set_button.pack(side=tk.BOTTOM, anchor=tk.E)
        
        self.set(data)
        
    def set(self, data: SettingData):
        data_set = map(
            lambda d, box: box.set(d) if box is not None else None,
            vars(data).values(), self.__boxes
        )
        list(data_set)
        
    def save(self, nodes: list, boxes: list):
        args = [*map(lambda box: box.value(), filter(lambda box: box is not None, boxes)), nodes]
        data = SettingData(*args)
        
        if messagebox.askyesno('注意', '設定を更新するためには、アプリを再起動しなければなりません。再起動しますか？'):
            Settings.save(SettingData.SETTINGFOLDER_PATH, data)
            Window.RunWindow(min(data.node_list), data)

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