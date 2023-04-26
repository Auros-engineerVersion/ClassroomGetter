import tkinter as tk

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
    def RunWindow(root_node, master: tk.Misc = None, width: int = 600, height: int = 300):        
        if master is None:
            master = tk.Tk()
        
        master.title('ClassroomHack')
        master.geometry(Window.__size(width, height))
        master.resizable(0, 0) #windowのサイズ変更を許可しない
        #アスペクト比を維持したまま小さいサイズにする
        node_canvas = mytk.ScrollableFrame(master, tk.SUNKEN, width=width/5, height=height/5, padx=1, pady=1)
        
        node_info = mytk.NodeInfoFrame(master)
        root_box = mytk.NodeBox(node_canvas.scrollable_frame, node_info, root_node) #最初の頂点を初期化, これは動的にpackされる
        node_info.set_box(root_box)
        
        node_canvas.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)
        node_info.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        master.mainloop()