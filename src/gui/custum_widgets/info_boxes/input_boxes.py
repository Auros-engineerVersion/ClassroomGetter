import tkinter as tk
from tkinter import filedialog
from pathlib import Path

BROWS = '参照'

class InputBox(tk.Frame):
    def __init__(self, master: tk.Misc, entry_or_spinbox = True, from_: int = 0, to: int = 60, width: int = 30, padx: tuple = (1, 1), title: str = 'title'):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text=title)
        self.input_box = \
            tk.Entry(self, width=width) if entry_or_spinbox\
            else tk.Spinbox(self, width=width, from_=from_, to=to)
        
        label.pack(side=tk.LEFT, anchor=tk.W, ipadx=1, padx=padx)
        self.input_box.pack(side=tk.LEFT, anchor=tk.E, ipadx= 1, padx=padx[:-1], expand=True) #tupleを反転させる

    def set(self, value):
        self.input_box.delete(0, tk.END)
        self.input_box.insert(0, value)
        
    def value(self):
        if type(self.input_box) == tk.Entry:
            return Path(self.input_box.get())
        else:
            return int(self.input_box.get())
            
class DialogInput(tk.Frame):
    def __init__(self, master: tk.Misc, width: int, default_path: Path, title: str = 'title'):
        tk.Frame.__init__(self, master)
        self.input_box = InputBox(self, width=width//8, title=title)
        brows_button = tk.Button(self, text=BROWS, command=self.folder_dialog)
        
        self.input_box.pack(side=tk.LEFT, expand=True)
        brows_button.pack(side=tk.RIGHT, anchor=tk.E)

        self.default_path = default_path
        
    def folder_dialog(self):
        folder_name = filedialog.askdirectory()
        if len(folder_name) > 0:
            self.input_box.set(folder_name)
        else:
            self.input_box.set(self.default_path.absolute())
            
    def set(self, path: Path):
        self.input_box.set(path)
        
    def value(self):
        return self.input_box.value()