import tkinter as tk

import custum_widgets as mytk
from browser.nodes import Node

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
    def RunWindow(master: tk.Misc = None, width: int = 600, height: int = 300, nodes: list = []):        
        if master is None:
            master = tk.Tk()
        
        master.title('ClassroomHack')
        master.geometry(Window.__size(width, height))
        master.resizable(0, 0) #windowのサイズ変更を許可しない
        #アスペクト比を維持したまま小さいサイズにする
        node_canvas = mytk.ScrollableFrame(master, width=width/5, height=height/5)
        
        root_node = min(nodes)
        Node.Serch(root_node)(lambda node:
            mytk.NodeBox(node_canvas.scrollable_frame, node).
            pack(side=tk.TOP, anchor=tk.W, padx=(node.tree_height*10, 0))
        )
        
        node_canvas.pack(side=tk.LEFT, fill=tk.Y)

        master.mainloop()