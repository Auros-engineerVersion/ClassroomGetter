import asyncio
import tkinter as tk

from ....data import *
from ..info_boxes import *


class NodeInfoFrame(tk.Frame):
    def __init__(self, master: tk.Misc, watching_box: NodeBox = None):
        tk.Frame.__init__(self, master, background='green')
        self.__watching_box = watching_box
        
        self.__node_name_label = tk.Label(self, text=watching_box.text if watching_box != None else NO_DATA)
        self.__node_url_label = tk.Label(self, text=watching_box.url if watching_box != None else NO_DATA)
        self.__time_box = Timer(self, watching_box=self.__watching_box)
        
        #ボタンが押されたら、監視中のNodeBoxからinitialize_treeを実行する
        self.__init_button = tk.Button(self, text=RUN)
        self.__init_button.bind(BUTTON_PRESS, lambda event: self.__watching_box.initialize_node())
        
#region pack
        self.__node_name_label.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=5)
        self.__node_url_label.pack(side=tk.TOP)
        self.__init_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.__time_box.pack(side=tk.BOTTOM)
#endregion
        
    def set_box(self, box: NodeBox):
        self.__node_name_label[TEXT] = box.text
        self.__node_url_label[TEXT] = box.url
        self.__watching_box = box
        self.__time_box.watching_box = box
        
    def change_state(self, state: str, text: str):
        self.__init_button[STATE] = state
        self.__init_button[TEXT] = text
        self.__init_button.update()
        
    async def run_clock_async(self, target: NodeBox):
        self.__watching_box = target
        self.__time_box.watching_box = target
        await self.__time_box.update_clock(target)
        
class Timer(tk.Frame):
    def __init__(self, master: tk.Misc, watching_box: NodeBox):
        tk.Frame.__init__(self, master, background='yellow')
        self.__watching_box = watching_box
        clock_frame = tk.Frame(self)
        clock_view  = tk.Label(clock_frame, text='次の更新まで')
        self.clock_label = tk.Label(clock_frame, text=NO_DATA)
                
        time_set_frame = tk.Frame(self)
        self.__time_setters = TimeSetters(self)
        set_button = tk.Button(time_set_frame, text='この時間に指定する')
        set_button.bind(BUTTON_PRESS, lambda event: self.__watching_box.set_time(RoutineData(*self.__time_setters.values())))
        
        reset_button = tk.Button(time_set_frame, text=RESET)
        reset_button.bind(BUTTON_PRESS, self.__watching_box.time_reset)
        
#region pack
        clock_frame.pack()
        clock_view.pack(side=tk.TOP)
        self.clock_label.pack(side=tk.TOP)
        
        time_set_frame.pack()
        self.__time_setters.pack()
        set_button.pack(side=tk.LEFT)
        reset_button.pack(side=tk.RIGHT)
#endregion
        
    @property
    def watching_box(self):
        return self.__watching_box
    
    @watching_box.setter
    def watching_box(self, box: NodeBox):
        self.__watching_box = box
        self.__time_setters.set(box.time)
        
    async def update_clock(self, box: NodeBox, interval: int):
        try:
            while not box.time.should_init():
                self.clock_label[TEXT] = box.time.remaine()
                await asyncio.sleep(interval)
                
            else:
                box.initialize_node()
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
        