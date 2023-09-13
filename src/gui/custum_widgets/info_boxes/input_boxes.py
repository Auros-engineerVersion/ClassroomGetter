import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from abc import ABCMeta, abstractmethod

from ...literals import *
from ....my_util import do_nothing, arrow

def box_factory(key_name, value):
    if type(value) == str:
        return lambda master: EntryInput(master, title=key_name)
    elif type(value) == int:
        return lambda master: SpinInput(master, from_to=(0, 256), title=key_name)
    elif type(value) == None or type(value) == set:
        return lambda master: None #この使われていないmasterは他のlambda関数と規格を合わせるために必要である
    else: #Pathなら
        return lambda master: DialogInput(master, default_path=value, title=key_name)

class InputBox(tk.Frame):
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
        tk.Entry(self).pack(side=tk.LEFT, anchor=tk.W)

class SpinInput(InputBox):
    def __init__(self, from_to: tuple[int, int], **kw) -> None:
        super().__init__(**kw)
        tk.Spinbox(self, from_=from_to[0], to=from_to[1]).pack(side=tk.LEFT, anchor=tk.W)
            
class DialogInput(InputBox):
    def __init__(self, default_path: Path, **kw):      
        super().__init__(**kw)
        tk.Entry(self)\
            |arrow| (lambda b: b.pack(side=tk.LEFT, anchor=tk.W))\
            |arrow| (lambda _: self.set(default_path.absolute()))
        
        #brows_button
        tk.Button(self, text=BROWS, command=self.folder_dialog).pack(side=tk.LEFT, anchor=tk.E, padx=kw.get('padx', 0))
        
    def folder_dialog(self):
        folder_name = filedialog.askdirectory()
        if len(folder_name) > 0:
            self.__box().set(folder_name)
        else:
            self.__box().set(self.__default_path.absolute())
    
class ProfileForm(tk.Frame):
    def __init__(self, master: tk.Misc):
        tk.Frame.__init__(self, master)
        
        self.__email    = EntryInput(self, title='email')
        self.__password = EntryInput(self, title='password')
        complete_button = tk.Button(self, text=COMPLETE, command=self.quit)
        master.protocol(WM_DELETE_WINDOW, lambda: self.__stop_or_continue(master))
        
#region pack
        self.__email.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.__password.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        complete_button.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5)
#endregion
    
    def __stop_or_continue(self, target: tk.Misc):
        ok_cancel = messagebox.askokcancel(
                title=WARNING,
                message=STOP_OR_CONTINUE,
            )
        
        if ok_cancel:
            target.destroy()
        else:
            do_nothing()
    
    def set(self, email: str, password: str):
        self.__email.set(email)
        self.__password.set(password)
        
    def value(self) -> tuple:
        return (self.__email.get(), self.__password.get())
    
    @staticmethod
    def pop_up(title: str):
        root = tk.Tk()
        root.title(title)
        form = ProfileForm(root)
        form.pack()
        
        form.mainloop()

        profile = None
        try:
            profile = form.value()
            root.destroy()
        except tk.TclError as e:
            raise e
            
        return profile