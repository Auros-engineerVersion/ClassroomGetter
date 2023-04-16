import tkinter as tk
import custum_widgets as mytk

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
    def RunWindow(master: tk.Misc = None, nodes: list = []):
        if master is None:
            master = tk.Tk()
        
        master.geometry(Window.__size(500, 300))
        master.resizable(0, 0) #windowのサイズ変更を許可しない

        node_canvas = mytk.ScrollableFrame(master)
        
        box = tk.Button(node_canvas.scrollable_frame, width=50)
        
        node_canvas.pack(side=tk.LEFT)
        box.pack(side=tk.LEFT)

        master.mainloop()