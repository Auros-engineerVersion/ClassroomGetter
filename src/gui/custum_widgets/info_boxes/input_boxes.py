import tkinter as tk
from abc import ABCMeta, abstractmethod
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Any

from ....literals import *
from ....my_util import CommentableObj, arrow, do_nothing


def box_factory(key_name, value):
    if isinstance(value, str):
        return lambda master: EntryInput(master=master, title=key_name)
    elif isinstance(value, int):
        return lambda master: SpinInput(from_to=(0, 256), master=master, title=key_name)
    elif isinstance(value, set):
        return lambda master: None #この使われていないmasterは他のlambda関数と規格を合わせるために必要である
    else: #Pathなら
        return lambda master: DialogInput(default_path=value, master=master, title=key_name)
    
class InputBase(metaclass=ABCMeta):
    @abstractmethod
    def set(self, value) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get(self):
        raise NotImplementedError

class InputBox(tk.Frame, InputBase):
    def __init__(self, **kw) -> None:
        tk.Frame.__init__(self, kw.get('master', tk.Tk))
        tk.Label(self, text=kw.get('title', self.__class__.__name__)).pack(side=tk.LEFT, anchor=tk.W)
        
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
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        tk.Entry(self).pack(side=tk.RIGHT, anchor=tk.E, fill=tk.X)

class SpinInput(InputBox):
    def __init__(self, from_to: tuple[int, int], **kw) -> None:
        super().__init__(**kw)
        tk.Spinbox(self, from_=from_to[0], to=from_to[1]).pack(side=tk.RIGHT, anchor=tk.E, fill=tk.X)
            
class DialogInput(InputBox):
    def __init__(self, default_path: Path, **kw):      
        super().__init__(**kw)
        tk.Entry(self)\
            |arrow| (lambda b: b.pack(side=tk.RIGHT, anchor=tk.E, fill=tk.X))\
            |arrow| (lambda _: self.set(default_path.absolute()))
        
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