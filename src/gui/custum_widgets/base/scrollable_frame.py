import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, master: tk.Misc, relief: str, padx: int, pady: int, bar_x = True, bar_y = True):
        tk.Frame.__init__(self, master, padx=padx, pady=pady, background='red')
        self.canvas = tk.Canvas(self, relief=relief, borderwidth=1)
        self.scrollable_frame = tk.Frame(self.canvas)
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
                
    #更新するかを検証する
    def validate_init(self, interval: int) -> bool:
        """
        Args:
        Returns:
            bool:初期化したならTrue、そうでないならFalse
        """
        self.__node.next_init_time = self.time
        
        if self.time.is_current() and self.time.should_init():
            self.__cancel_all()
            self.initialize_node()
        
        self.__events.append(self.after(interval, self.validate_init, interval)) #再び繰り返す