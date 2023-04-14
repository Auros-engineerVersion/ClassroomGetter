import tkinter as tk
from tkinter import ttk

class Window(tk.Frame):
    @staticmethod
    def InputForm(func = None, *args, master: tk.Misc = None):
        def __function_is_not_null(func = None, *args):
            if (func != None):
                return func(*args)
                
        if (master == None):
            master = tk.Tk()
        
        master.title('title')
        master.resizable(0, 0) #windowのサイズ変更を許可しない
        
        padx_size = (5, 10)
        width      = 30
        
        email = Window.InputBox(master, width, padx_size, 'email')
        password = Window.InputBox(master, width, padx_size, 'password')
        complete_button = tk.Button(master, text='完了', command=lambda:__function_is_not_null(func, *args))

        # ウィジェットの配置
        email.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        password.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        complete_button.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5)
        
        master.mainloop()
        
        complete_button.
            
    @staticmethod
    def InputBox(master: tk.Misc, width: int, padx: int, title = '') -> tk.Frame:
        frame = tk.Frame(master)
        label = tk.Label(frame, text=title)
        t_box = tk.Entry(frame, width=width)
        
        label.pack(side=tk.LEFT, anchor=tk.W, ipadx=1, padx=padx)
        t_box.pack(side=tk.RIGHT, anchor=tk.E, ipadx= 1, padx=padx[:-1]) #tupleを反転させる
        
        return frame
    
if __name__ == '__main__':
    Window.InputForm()