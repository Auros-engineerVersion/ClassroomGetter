import asyncio
import tkinter as tk

from ....data import *
from ....literals import *
from ....my_util import arrow, is_none
from ..info_boxes import *


class NodeInfoFrame(tk.Frame):
    def __init__(self, master: tk.Misc, watching_box: NodeBox = None):
        tk.Frame.__init__(self, master, background='green')
        self.__watching_box = watching_box
        
        #keyの表示
        self.__key_label = tk.Label(self, text=is_none(watching_box.text, NO_DATA))\
            |arrow| (lambda l: l.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=5))
            
        #urlの表示
        self.__url_label = tk.Label(self, text=is_none(watching_box.url, NO_DATA))\
            |arrow| (lambda l: l.pack(side=tk.TOP))
            
        #ボタンが押されたら、監視中のNodeBoxからinitialize_treeを実行する
        self.__init_button = tk.Button(self, text=RUN)\
            |arrow| (lambda b: b.pack(side=tk.BOTTOM, fill=tk.X))\
            |arrow| (lambda b: b.bind(BUTTON_PRESS, lambda _: 
                self.__watching_box.initialize()))
            
        #保存の際、そのNodeをパスに含めるかどうかを設定する
        self.__check_var = tk.BooleanVar(value=watching_box.include_this_to_path)
        tk.Checkbutton(self,
            text=INCLUDE_THIS_IN_PATH,
            variable=self.__check_var,
            command=lambda: self.on_change_check_value(self.__check_var))\
            |arrow| (lambda c: c.pack(side=tk.BOTTOM, fill=tk.X))
                        
        #次回の更新までの時間を表示する
        self.__time_box: Timer = Timer(self, watching_box=self.__watching_box)\
            |arrow| (lambda t: t.pack(side=tk.TOP))
        
    def set_box(self, box: NodeBox):
        self.__key_label[TEXT] = box.text
        self.__url_label[TEXT] = box.url
        self.__check_var.set(box.include_this_to_path)
        self.__watching_box = box
        self.__time_box.watching_box = box
        
    def on_change_check_value(self, boolean_var: tk.BooleanVar):
        self.__watching_box.include_this_to_path = boolean_var.get()
        
    def change_state(self, state: str, text: str):
        self.__init_button[STATE] = state
        self.__init_button[TEXT] = text
        self.__init_button.update()
        
    async def run_clock_async(self, target: NodeBox):
        self.__watching_box = target
        self.__time_box.watching_box = target
        await self.__time_box.update_clock(target.time, target.initialize_tree, 1)
        
class Timer(tk.Frame):
    def __init__(self, master: tk.Misc, watching_box: NodeBox):
        tk.Frame.__init__(self, master, background='yellow')
        self.__watching_box = watching_box
        
        clock_frame = tk.Frame(self)\
            |arrow| (lambda f: f.pack())
            
        #時計の表示の文字
        tk.Label(clock_frame, text='次の更新まで')\
            |arrow| (lambda l: l.pack(side=tk.TOP))
            
        self.clock_label = tk.Label(clock_frame, text=NO_DATA)\
            |arrow| (lambda l: l.pack(side=tk.TOP))
                
        time_set_frame = tk.Frame(self)\
            |arrow| (lambda f: f.pack())
            
        #時間の設定ボタン群
        self.__time_setters = TimeSetters(self)\
            |arrow| (lambda t: t.pack(side=tk.LEFT))
        
        #時間指定ボタン    
        tk.Button(time_set_frame, text='この時間に指定する')\
            |arrow| (lambda b: b.pack(side=tk.RIGHT))\
            |arrow| (lambda b: b.bind(BUTTON_PRESS, 
                lambda _: self.__watching_box.set_time(RoutineData(*self.__time_setters.values()))))
        
        #時間のリセット
        tk.Button(time_set_frame, text=RESET)\
            |arrow| (lambda b: b.pack(side=tk.RIGHT))\
            |arrow| (lambda b: b.bind(BUTTON_PRESS, self.__watching_box.time_reset))
        
    @property
    def watching_box(self):
        return self.__watching_box
    
    @watching_box.setter
    def watching_box(self, box: NodeBox):
        self.__watching_box = box
        self.__time_setters.set(box.time)
        
    #
    #interval: 
    async def update_clock(self, dead_line: IRoutineData, complete_func, interval: int):
        """boxの時間を監視し、時間が来たらboxのinitialize_treeを実行する

        Args:
            dead_line (IRoutineData): 残り時間
            complete_func (Callable): 時間が来た時に実行する関数
            interval (int): 監視する間隔
        """
        try:
            while not dead_line.should_init():
                self.clock_label[TEXT] = dead_line.remaine()
                await asyncio.sleep(interval)
                
            else:
                complete_func()
        except asyncio.CancelledError:
            return

class TimeSetters(tk.Frame):
    def __init__(self, master: tk.Misc):
        tk.Frame.__init__(self, master)
        self.__boxes = list(
            map(
                lambda items, range: SpinInput(from_to=range, master=self, title=items[0]),
                vars(RoutineData()).items(), RoutineData.time_range
            )
        )
        
        for box in self.__boxes:
            box.pack()
                    
    def values(self) -> RoutineData:
        return RoutineData(*map(lambda box: int(box.get()), self.__boxes))
        
    def set(self, time: RoutineData):
        tmp = map(
            lambda box, value: box.set(value),
            self.__boxes, vars(time).values()
        )
        list(tmp)
        