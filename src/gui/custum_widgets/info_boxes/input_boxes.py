import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from ....literals import *
from ....my_util import arrow
from ....interface import InputBase

def box_factory(master, key_name, value):
    if isinstance(value, str):
        return EntryInput(master=master, title=key_name, default=value)
    elif isinstance(value, int):
        return SpinInput(from_to=(0, 256), master=master, title=key_name, default=value)
    elif isinstance(value, set):
        return None
    else: #Pathなら
        return DialogInput(master=master, title=key_name, default=value)

class InputBox(tk.Frame, InputBase):
    def __init__(self, title, **kw) -> None:
        tk.Frame.__init__(self, **kw)
        tk.Label(self, text=title).pack(side=tk.LEFT, anchor=tk.W)
        
    def __box(self):
        boxes = list(filter(lambda x: isinstance(x, (tk.Entry, tk.Spinbox)), self.children.values()))
        if len(boxes) < 1:
            raise ValueError('InputBoxの子供が見つかりませんでした')
        elif len(boxes) > 1:
            raise ValueError('InputBoxの子供が複数見つかりました')
        else:
            return boxes[0]
        
    def set(self, value) -> None:
        self.__box()\
            |arrow| (lambda b: b.delete(0, tk.END))\
            |arrow| (lambda b: b.insert(0, value))
    
    def get(self):
        return self.__box().get()

class EntryInput(InputBox):
    def __init__(self, title, default=NO_DATA, **kw) -> None:
        super().__init__(title, **kw)
        tk.Entry(self).pack(side=tk.RIGHT, anchor=tk.E, fill=tk.X)
        self.set(default)

class SpinInput(InputBox):
    def __init__(self, title, from_to: tuple[int, int], default=NO_DATA, **kw) -> None:
        super().__init__(title, **kw)
        tk.Spinbox(self, from_=from_to[0], to=from_to[1]).pack(side=tk.RIGHT, anchor=tk.E, fill=tk.X)
        self.set(default)
            
class DialogInput(InputBox):
    def __init__(self, title, default=NO_DATA, **kw):      
        super().__init__(title, **kw)
        tk.Entry(self).pack(side=tk.RIGHT, anchor=tk.E, fill=tk.X)
        self.set(default)
        
        #brows_button
        tk.Button(self, text=BROWS, command=self.folder_dialog).pack(side=tk.LEFT, anchor=tk.E, padx=kw.get('padx', 0))
        
    def folder_dialog(self):
        folder_name = filedialog.askdirectory()
        if len(folder_name) > 0:
            self.__box().set(folder_name)
        else:
            self.__box().set(self.__default_path.absolute())
    
class ProfileForm(tk.Frame, InputBase):
    def __init__(self, master: tk.Misc = None):
        if master == None:
            master = tk.Tk()\
                |arrow| (lambda m: m.title('ProfileForm'))
            tk.Frame.__init__(self, master)
            self.pack()
        else:
            master.title('ProfileForm')
            tk.Frame.__init__(self, master)
        
        self.__email = EntryInput(master=self, title='email')\
            |arrow| (lambda e: e.pack(side=tk.TOP, anchor=tk.W, fill=tk.X))

        self.__password = EntryInput(master=self, title='password')\
            |arrow| (lambda p: p.pack(side=tk.TOP, anchor=tk.W, fill=tk.X))
            
        #ボタンフレーム
        button_frame = tk.Frame(self)\
            |arrow| (lambda f: f.pack(side=tk.TOP, anchor=tk.W, fill=tk.X))
            
        #完了ボタン
        tk.Button(button_frame, text=COMPLETE)\
            |arrow| (lambda b: b.pack(side=tk.RIGHT, anchor=tk.E, padx=5, pady=5))\
            |arrow| (lambda b: b.bind(BUTTON_PRESS, lambda _: self.quit()))
            
        #ゲストモード
        tk.Button(button_frame, text=GUEST_MODE)\
            |arrow| (lambda b: b.pack(side=tk.RIGHT, anchor=tk.E, padx=5, pady=5))\
            |arrow| (lambda b: b.bind(BUTTON_PRESS, lambda _: self.set('guest', 'guest') |arrow| (lambda _: self.quit())))
            
        master.protocol(WM_DELETE_WINDOW, lambda: self.__stop_or_continue(master))
    
    def __stop_or_continue(self, target: tk.Misc):
        ok_cancel = messagebox.askokcancel(
                title=WARNING,
                message=STOP_OR_CONTINUE,
            )
        
        if ok_cancel:
            target.destroy()
    
    def set(self, email: str, password: str):
        self.__email.set(email)
        self.__password.set(password)
        
    def get(self) -> tuple:
        return (self.__email.get(), self.__password.get())
    
    def pop_up(self, loop = lambda x: x.winfo_toplevel().mainloop()):
        loop(self)
        
        #途中で終了していたら
        if len(self.children) < 1:
            raise ChildProcessError
        
        profile = self.get()
        self.winfo_toplevel().destroy()

        return profile