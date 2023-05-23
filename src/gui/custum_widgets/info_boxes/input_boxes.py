import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from abc import ABCMeta, abstractmethod

BROWS = '参照'

def box_factory(key_name, value, width: int):
    if type(value) == str:
        return lambda master: EntryInput(master, width=width, entry_or_spinbox=True, title=key_name)
    elif type(value) == int:
        return lambda master: SpinInput(master, width=width, entry_or_spinbox=False, title=key_name)
    elif type(value) == None or type(value) == set:
        return lambda master: None #この使われていないmasterは他のlambda関数と規格を合わせるために必要である
    else: #Pathなら
        return lambda master: DialogInput(master, width=width, default_path=value, title=key_name)

class InputBox(tk.Frame, metaclass=ABCMeta):
    def __init__(self, master: tk.Misc, padx: tuple = (1, 1), title: str = 'title') -> None:
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text=title)
        label.pack(side=tk.LEFT, anchor=tk.W, ipadx=1, padx=padx)
        
    @abstractmethod
    def set(self, value) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def value(self) -> str | int | Path:
        raise NotImplementedError

class EntryInput(InputBox):
    def __init__(self, master: tk.Misc, width: int=30, padx: tuple = (1, 1), title: str = 'title') -> None:
        super().__init__(master, padx, title)
        self.__entry = tk.Entry(self, width=width)
        self.__entry.pack(side=tk.RIGHT)
    
    def set(self, value):
        self.__entry.delete(0, tk.END)
        self.__entry.insert(0, value)
        
    def value(self) -> str:
        return self.__entry.get()
    
class SpinInput(InputBox):
    def __init__(self, master: tk.Misc, from_to: tuple[int, int],  width: int=30, padx: tuple = (1, 1), title: str = 'title') -> None:
        super().__init__(master, padx, title)
        
        self.__spin = tk.Spinbox(self, width=width, from_=from_to[0], to=from_to[1])
        self.__spin.pack(side=tk.RIGHT)
        
    def set(self, value: int) -> None:
        self.__spin.delete(0, tk.END)
        self.__spin.insert(0, value)
            
    def value(self) -> int:
        return int(self.__spin.get())
            
class DialogInput(InputBox):
    def __init__(self, master: tk.Misc, default_path: Path, width: int=30, padx: tuple = (1, 1), title: str = 'title'):
        super().__init__(master, padx, title)
        brows_button = tk.Button(self, text=BROWS, command=self.folder_dialog)
        self.__entry = tk.Entry(self, width=width//8)
        
        brows_button.pack(side=tk.RIGHT, anchor=tk.E)           
        self.__entry.pack(side=tk.RIGHT, expand=True)

        self.__default_path = default_path
        
    def folder_dialog(self):
        folder_name = filedialog.askdirectory()
        if len(folder_name) > 0:
            self.input_box.set(folder_name)
        else:
            self.input_box.set(self.__default_path.absolute())
            
    def set(self, path: Path):
        self.__entry.delete(0, tk.END)
        self.__entry.insert(0, path)
        
    def value(self):
        return self.__entry.get()
    
class ProfileForm(tk.Frame):
    def __init__(self, master: tk.Misc):
        tk.Frame.__init__(self, master)
        
        padx_size = (5, 10)
        width = 30

        self.__email    = EntryInput(self, width=width, padx=padx_size, title='email')
        self.__password = EntryInput(self, width=width, padx=padx_size, title='password')
        complete_button = tk.Button(self, text='完了', command=self.quit)
        
#region pack
        self.__email.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.__password.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        complete_button.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5)
#endregion

    def set(self, email: str, password: str):
        self.__email.set(email)
        self.__password.set(password)
        
    def value(self) -> tuple:
        return (self.__email.value(), self.__password.value())
    
    @staticmethod
    def pop_up(title: str):
        root = tk.Tk()
        root.title(title)
        form = ProfileForm(root)
        form.pack()
        
        form.mainloop()

        profile = form.value()
        root.destroy()
        return profile