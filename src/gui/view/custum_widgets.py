from __future__ import annotations
import gc
import tkinter as tk
from tkinter import filedialog
from datetime import timedelta
from pathlib import Path

from src.interface.i_node import INode
from src.data.routine_data import RoutineData

BUTTON_PRESS = "<ButtonPress>"
TEXT = "text"
TEXT_VARIABLE = 'textvariable'
STATE = 'state'
NO_DATA = '未設定'
RUN = '実行'
LOADING = '更新中'
BROWS = '参照'

def box_factory(key_name, value, width: int):
    if type(value) == str:
        return lambda master: InputBox(master, width=width, entry_or_spinbox=True, title=key_name)
    elif type(value) == int:
        return lambda master: InputBox(master, width=width, entry_or_spinbox=False, title=key_name)
    elif type(value) == None or type(value) == set:
        return lambda master: None #この使われていないmasterは他のlambda関数と規格を合わせるために必要である
    else: #Pathなら
        return lambda master: DialogInput(master, width=width, default_path=value, title=key_name)

class ScrollableFrame(tk.Frame):
    def __init__(self, master: tk.Misc, relief: str, width: int, height: int, padx: int, pady: int, bar_x = True, bar_y = True):
        tk.Frame.__init__(self, master, width=width, height=height, padx=padx, pady=pady, background='red')
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
            
class NodeBox(tk.Frame):
    def __init__(self, master: tk.Misc, node_info_frame: NodeInfoFrame, node: INode, parent: NodeBox = None):
        tk.Frame.__init__(self, master)
        self.time: RoutineData = node.next_init_time
        self.__master = master
        self.__node_info_frame = node_info_frame
        self.__parent_box = parent
        self.__node = node
        self.__is_expand: bool = False
        self.__nextboxes: list[NodeBox] = []
        self.__events: list[str] = [] #afterのリスト
        
        drop_button = tk.Button(self, command=self.expand, width=self.winfo_height())
        height_label = tk.Label(self, text=str(node.tree_height) + ':')
        key_label = tk.Label(self, text=str(node.key))
        
        drop_button.pack(side=tk.LEFT)
        height_label.pack(side=tk.LEFT)
        key_label.pack(side=tk.LEFT)
        
        height_label.bind(BUTTON_PRESS, self.on_frame_click)        
        key_label.bind(BUTTON_PRESS, self.on_frame_click)
        
        self.pack(anchor=tk.W, padx=(node.tree_height*20, 1), after=self.__parent_box)
        
        self.text = key_label[TEXT]
        self.url = node.url
    
    #すべてのafterをキャンセルする
    def __cancel_all(self):
        for id in self.__events:
            self.after_cancel(id)
        self.__events.clear()
    
    def on_frame_click(self, event):
        self.__node_info_frame.set_box(self)
        
    def dispose(self):
        stack: list[NodeBox] = [self]
        while(len(stack) > 0):
            value = stack.pop()
            
            for box in value.__nextboxes:
                stack.append(box)

            value.destroy()
        
    def initialize_node(self):
        self.__node_info_frame.change_state(tk.DISABLED, LOADING) #表示を変える
        self.__node.edges().clear()
        self.__node.initialize_tree()
        self.__is_expand = False
        self.__node_info_frame.change_state(tk.NORMAL, RUN)
                    
    def expand(self):
        #反転する
        self.__is_expand = not self.__is_expand
        
        #子を初期化する
        for next in self.__nextboxes:
            next.dispose()
        self.__nextboxes.clear()
        gc.collect()
        
        if self.__is_expand:
            self.pack(anchor=tk.W)
            for node in self.__node.edges():
                new_box = NodeBox(self.__master, self.__node_info_frame, node, self)
                self.__nextboxes.append(new_box)
                
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
        
class NodeInfoFrame(tk.Frame):
    def __init__(self, master: tk.Misc, watching_box: NodeBox = None):
        tk.Frame.__init__(self, master, background='green')
        self.__watching_box = watching_box
        
        self.__node_name_label = tk.Label(self, text=watching_box.text if watching_box != None else NO_DATA)
        self.__node_url_label = tk.Label(self, text=watching_box.url if watching_box != None else NO_DATA)
        self.__time_box = TimeBox(self, watching_box=self.__watching_box)
        
        #ボタンが押されたら、監視中のNodeBoxからinitialize_treeを実行する
        self.__init_button = tk.Button(self,
            text=RUN,
            command=lambda: self.__watching_box.initialize_node()
        )
        
        self.__node_name_label.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=5)
        self.__node_url_label.pack(side=tk.TOP)
        self.__init_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.__time_box.pack(side=tk.BOTTOM)
        
    def set_box(self, box: NodeBox):
        self.__node_name_label[TEXT] = box.text
        self.__node_url_label[TEXT] = box.url
        self.__watching_box = box
        self.__time_box.set_box(box)
        
    def change_state(self, state: str, text: str):
        self.__init_button[STATE] = state
        self.__init_button[TEXT] = text
        self.__init_button.update()
        
class TimeBox(tk.Frame):
    def __init__(self, master: tk.Misc, watching_box: NodeBox):
        tk.Frame.__init__(self, master, background='yellow')
        self.__clocK_update_interval = 1000 #ms
        self.__watching_box = watching_box
        self.__events: list[str] = []

        clock_frame = tk.Frame(self)
        clock_view  = tk.Label(clock_frame, text='次の更新まで')
        self.clock_label = tk.Label(clock_frame, text=NO_DATA)
                
        time_set_frame = tk.Frame(self)
        self.__time_setters = TimeSetters(self)
        set_button = tk.Button(
            time_set_frame, 
            text='この時間に指定する',
            command=lambda: self.__set_date(RoutineData(*self.__time_setters.values()))
        )
        reset_button = tk.Button(
            time_set_frame,
            text='元に戻す',
            command=lambda: self.__set_date(RoutineData())
        )
        
        clock_frame.pack()
        clock_view.pack(side=tk.TOP)
        self.clock_label.pack(side=tk.TOP)
        
        time_set_frame.pack()
        self.__time_setters.pack()
        set_button.pack(side=tk.LEFT)
        reset_button.pack(side=tk.RIGHT)
        
    def __cancel_all(self):
        for id in self.__events:
            self.after_cancel(id)
        self.__events.clear()
        
    def __update_clock(self, box: NodeBox, interval: int):
        remaine_time = box.time.remaine()
        if remaine_time == timedelta():
            self.clock_label[TEXT] = NO_DATA
        else:
            self.clock_label[TEXT] = remaine_time
            
        self.__events.append(self.after(interval, self.__update_clock, box, interval))
        
    def __set_date(self, data: RoutineData):
        self.__watching_box.time = data 
        self.__watching_box.validate_init(interval=self.__clocK_update_interval)
        
    def set_box(self, box: NodeBox): #時計の更新を行う
        self.__watching_box = box
        self.__cancel_all()
        self.__update_clock(box, self.__clocK_update_interval)

class TimeSetters(tk.Frame):
    def __init__(self, master: tk.Misc):
        tk.Frame.__init__(self, master)
        self.week_setter   = InputBox(self, False, title='週', from_=0, to=6)
        self.day_setter    = InputBox(self, False, title='日', from_=0, to=31)
        self.hour_setter   = InputBox(self, False, title='時', from_=0, to=23)
        self.minute_setter = InputBox(self, False, title='分', from_=0, to=59)
        
        self.week_setter.pack()
        self.day_setter.pack()
        self.hour_setter.pack()
        self.minute_setter.pack()
        
    def values(self):
        return [
            int(self.week_setter.value()),
            int(self.day_setter.value()),
            int(self.hour_setter.value()),
            int(self.minute_setter.value())
        ]
        
    def set_values(self, time: RoutineData):
        self.week_setter.set(time.week)
        self.day_setter.set(time.day)
        self.hour_setter.set(time.hour)
        self.minute_setter.set(time.minute)