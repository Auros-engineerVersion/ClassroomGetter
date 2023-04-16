import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, master: tk.Misc, width: int, height: int, bar_x = True, bar_y = True):
        tk.Frame.__init__(self, master)
        self.canvas = tk.Canvas(self)
        self.scrollable_frame = tk.Frame(self.canvas, width=width, height=height)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox(tk.ALL)
            )
        )
                
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        if bar_y:
            self.scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        if bar_x:
            self.scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
            self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
            
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

class InputBox(tk.Frame):
    def __init__(self, master: tk.Misc, width: int = 30, padx: tuple = (1, 1), title: str = 'title'):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text=title)
        t_box = tk.Entry(self, width=width)
        
        label.pack(side=tk.LEFT, anchor=tk.W, ipadx=1, padx=padx)
        t_box.pack(side=tk.RIGHT, anchor=tk.E, ipadx= 1, padx=padx[:-1]) #tupleを反転させる
            
class NodeBox(tk.Button):
    def __init__(self, master: tk.Misc, node):
        tk.Button.__init__(self, master) #tree_heightに応じてインデントする
        height_label = tk.Label(self, text=str(node.tree_height) + ':')
        url_label = tk.Label(self, text=str(node.key))
        
        height_label.pack(side=tk.LEFT)
        url_label.pack(side=tk.LEFT)