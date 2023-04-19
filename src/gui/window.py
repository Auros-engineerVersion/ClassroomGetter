import tkinter as tk

from src.gui import custum_widgets as mytk
from src.setting.setting_data import SettingData

class Window(tk.Frame):
    @staticmethod
    def __get_data(frame: tk.Frame):
        for child in frame.winfo_children():
            if (type(child) == tk.Entry):
                return child.get()
            
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
        
        email    = mytk.InputBox(master, width, padx_size, 'email')
        password = mytk.InputBox(master, width, padx_size, 'password')
        complete_button = tk.Button(master, text='完了', command=master.quit)

        # ウィジェットの配置
        email.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        password.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        complete_button.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5)
        
        master.mainloop()
                
        #入力された値を取得して返す
        email_info     = Window.__get_data(email)
        password_info  = Window.__get_data(password)
        master.destroy() #値を取得できたらフォームを解放する
        return (email_info, password_info)
            
    @staticmethod
    def RunWindow(root_node, master: tk.Misc = None, width: int = 600, height: int = 300):        
        if master is None:
            master = tk.Tk()
        
        master.title('ClassroomHack')
        master.geometry(Window.__size(width, height))
        master.resizable(0, 0) #windowのサイズ変更を許可しない
        #アスペクト比を維持したまま小さいサイズにする
        node_canvas = mytk.ScrollableFrame(master, tk.SUNKEN, width=width/5, height=height/5, padx=1, pady=1)
        
        root_box = mytk.NodeBox(node_canvas.scrollable_frame, root_node) #最初の頂点を初期化
        node_info = mytk.NodeInfoFrame(master, root_box)
        mytk.NodeBox.node_info_box = node_info
        
        node_canvas.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)
        node_info.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        master.mainloop()