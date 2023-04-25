from __future__ import annotations
import gc
import tkinter as tk
from datetime import datetime
from time import sleep

from src.interface.i_node import INode
from src.data.routine_data import RoutineData

BUTTON_PRESS = "<ButtonPress>"
TEXT = "text"
TEXT_VARIABLE = 'textvariable'
STATE = 'state'
NO_DATA = '未設定'

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
    def __init__(self, master: tk.Misc, entry_or_spinbox = True, from_: int = 0, to: int = 0, width: int = 30, padx: tuple = (1, 1), title: str = 'title'):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text=title)
        self.input_box = tk.Entry(self, width=width) if entry_or_spinbox else tk.Spinbox(self, width=width, from_=from_, to=to)
        
        label.pack(side=tk.LEFT, anchor=tk.W, ipadx=1, padx=padx)
        self.input_box.pack(side=tk.RIGHT, anchor=tk.E, ipadx= 1, padx=padx[:-1]) #tupleを反転させる
        
    def value(self):
        return self.input_box.get()
            
    def set(self, variable):
        self.input_box[TEXT_VARIABLE] = variable
            
class NodeBox(tk.Frame):
    node_info_box: NodeInfoFrame = None
    def __init__(self, master: tk.Misc, node: INode, parent: NodeBox = None):
        tk.Frame.__init__(self, master)
        drop_button = tk.Button(self, command=self.expand, width=self.winfo_height())
        height_label = tk.Label(self, text=str(node.tree_height) + ':')
        key_label = tk.Label(self, text=str(node.key))
        url_label = tk.Label(self, text=str(node.url))
        
        drop_button.pack(side=tk.LEFT)
        height_label.pack(side=tk.LEFT)
        key_label.pack(side=tk.LEFT)
        url_label.pack(side=tk.LEFT)
        
        height_label.bind(BUTTON_PRESS, self.on_frame_click)        
        key_label.bind(BUTTON_PRESS, self.on_frame_click)
        url_label.bind(BUTTON_PRESS, self.on_frame_click)
            
        self.text = key_label[TEXT]
        self.__master = master
        self.__parent_box = parent
        self.__node = node
        self.__is_expand: bool = False
        self.__nextboxes: list[NodeBox] = []
        
        self.pack(anchor=tk.W, padx=(node.tree_height*20, 1), after=self.__parent_box)
    
    def node(self):
        return self.__node

    def on_frame_click(self, event):
        self.node_info_box.update_text(self)
        
    def dispose(self):
        stack: list[NodeBox] = [self]
        while(len(stack) > 0):
            value = stack.pop()
            
            for box in value.__nextboxes:
                stack.append(box)

            value.destroy()
        
    def initialize(self, state: str):
        self.__node.edges().clear()
        self.__node.initialize_tree()
        self.__is_expand = False
                    
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
                new_box = NodeBox(self.__master, node, self)
                self.__nextboxes.append(new_box)
        
class NodeInfoFrame(tk.Frame):
    def __init__(self, master: tk.Misc, watching_box: NodeBox = None):
        tk.Frame.__init__(self, master, background='green')
        
        self.__watching_box = watching_box
        self.__node_name_label = tk.Label(self, text=watching_box.text if watching_box.text != None else 'No Data')
        self.__time_box = TimeBox(self)
        
        #ボタンが押されたら、監視中のNodeBoxからinitialize_treeを実行する
        self.__init_button = tk.Button(self,
            text='実行', 
            command=lambda: self.__run_initialize(self.__init_button[STATE])
        )
        
        self.__node_name_label.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=5)
        self.__init_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.__time_box.pack(side=tk.BOTTOM)
        
    def __run_initialize(self, state: str):
        def __change_state(state: str):
            self.__init_button[STATE] = state
        #通常状態からボタンが押されたら
        if state == tk.NORMAL:
            __change_state(tk.DISABLED)
            self.__watching_box.initialize()
        elif state == tk.DISABLED:
            __change_state(tk.NORMAL)
        
    def update_text(self, target_box: NodeBox):
        self.__watching_box = target_box
        self.__node_name_label[TEXT] = target_box.text
        self.__time_box.update_clock(target_box.node().next_init_time)

class TimeBox(tk.Frame):
    def __init__(self, master: tk.Misc):
        tk.Frame.__init__(self, master, background='yellow')

        clock_frame = tk.Frame(self)
        clock_view  = tk.Label(clock_frame, text='次の更新まで')
        self.clock_label = tk.Label(clock_frame, text=NO_DATA)
                
        time_set_frame = tk.Frame(self)
        time_setters = TimeSetters(self)
        set_button = tk.Button(
            time_set_frame, 
            text='この時間に指定する',
            command=lambda: self.set_date(RoutineData(*time_setters.values()))
        )
        
        clock_frame.pack()
        clock_view.pack(side=tk.TOP)
        self.clock_label.pack(side=tk.TOP)
        
        time_set_frame.pack()
        time_setters.pack()
        set_button.pack()
        
        self.__events: list[str] = [] #afterのリスト
                
    def __del__(self):
        self.__cancel_all()
            
    def __cancel_all(self):
        for id in self.__events:
            self.after_cancel(id)
        self.__events.clear()
        
    def update_clock(self, time_date: RoutineData):
        if time_date.should_init():
            self.clock_label[TEXT] = NO_DATA
        else:
            self.clock_label[TEXT] = str(time_date.remaine_time()) #現在時刻との差分を表示する
        
    #N秒ごとに文字盤を更新する
    def update_event(self, time_date: RoutineData, wait_time: int = 1000):
        self.update_clock(time_date)
        self.__events.append(self.after(wait_time, self.update_event, time_date))

    def set_date(self, time: RoutineData):
        self.__cancel_all()
        self.update_event(time)

class TimeSetters(tk.Frame):
    def __init__(self, master: tk.Misc):
        tk.Frame.__init__(self, master)
        self.month_setter  = InputBox(self, False, title='月', from_=0, to=12)
        self.week_setter   = InputBox(self, False, title='週', from_=0, to=6)
        self.day_setter    = InputBox(self, False, title='日', from_=0, to=31)
        self.hour_setter   = InputBox(self, False, title='時', from_=0, to=23)
        self.minute_setter = InputBox(self, False, title='分', from_=0, to=59)
        
        self.month_setter.pack()
        self.week_setter.pack()
        self.day_setter.pack()
        self.hour_setter.pack()
        self.minute_setter.pack()
        
    def values(self):
        return [
            0, #年は0とする
            int(self.month_setter.value()),
            int(self.week_setter.value()),
            int(self.day_setter.value()),
            int(self.hour_setter.value()),
            int(self.minute_setter.value())
        ]
        
    def set_values(self, time: RoutineData):
        self.month_setter.set(time.month)
        self.week_setter.set(time.week)
        self.day_setter.set(time.day)
        self.hour_setter.set(time.hour)
        self.minute_setter.set(time.minute)