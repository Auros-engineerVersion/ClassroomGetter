import tkinter as tk
from tkinter import ttk

class Window(tk.Frame):
    @staticmethod
    def __GetData(frame: tk.Frame):
        for child in frame.winfo_children():
            if (type(child) == tk.Entry):
                return child.get()
    
    @staticmethod
    def InputForm(master: tk.Misc = None) -> tuple:
        if (master == None):
            master = tk.Tk()
        
        master.title('title')
        master.resizable(0, 0) #windowのサイズ変更を許可しない
        
        padx_size = (5, 10)
        width = 30
        
        email = Window.InputBox(master, width, padx_size, 'email')
        password = Window.InputBox(master, width, padx_size, 'password')
        complete_button = tk.Button(master, text='完了', command=master.quit)

        # ウィジェットの配置
        email.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        password.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        complete_button.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5)
        
        master.mainloop()
                
        #入力された値を取得して返す
        email_info = Window.__GetData(email)
        password_info = Window.__GetData(password)
        master.destroy() #値を取得できたらフォームを解放する
        return (email_info, password_info)
            
    @staticmethod
    def InputBox(master: tk.Misc, width: int, padx: int, title = '') -> tk.Frame:
        frame = tk.Frame(master)
        label = tk.Label(frame, text=title)
        t_box = tk.Entry(frame, width=width)
        
        label.pack(side=tk.LEFT, anchor=tk.W, ipadx=1, padx=padx)
        t_box.pack(side=tk.RIGHT, anchor=tk.E, ipadx= 1, padx=padx[:-1]) #tupleを反転させる
                
        return frame

if __name__ == '__main__':
    for value in Window.InputForm():
        print(value)