import tkinter as tk
from tkinter import ttk

class WindowData(tk.Frame):
    def __init__(self, master = None) -> None:
        super().__init__(master)
        
        self.master.geometry('256x256')
        
        email = self.InputBox(self.master, 30, 1, 'email')
        password = self.InputBox(self.master, 10, 1, 'password')

        # ウィジェットの配置
        email.pack(side=tk.TOP, anchor=tk.W)
        password.pack(side=tk.TOP, anchor=tk.W)
    
    @staticmethod
    def InputBox(master: tk.Misc, width: int, height: int, text = '') -> tk.Frame:
        frame = tk.Frame(master)
        label = tk.Label(frame, text=text)
        t_box = tk.Text(frame, width=width, height=height)
        
        label.pack(anchor=tk.W, ipadx=1)
        t_box.pack(anchor=tk.E, ipadx= 1)
        
        return frame
    
if __name__ == '__main__':
    WindowData(master=tk.Tk()).mainloop()