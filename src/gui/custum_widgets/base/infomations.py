import tkinter as tk
import asyncio

from src.data.routine_data import RoutineData, timedelta
from src.gui.custum_widgets.info_boxes.node_box import NodeBox
from src.gui.custum_widgets.info_boxes.input_boxes import SpinInput

TEXT = "text"
STATE = 'state'
NO_DATA = '未設定'
RUN = '実行'

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
            command=lambda: asyncio.run(self.__watching_box.initialize_node())
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
            command=lambda: self.__set_dateself.__time_setters.values()
        )
        
        reset_button = tk.Button(
            time_set_frame,
            text='元に戻す',
            command=lambda: self.__set(RoutineData())
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
        
    def __set(self, data: RoutineData):
        self.__watching_box.time = data 
        self.__watching_box.validate_init(interval=self.__clocK_update_interval)
        
    def set_box(self, box: NodeBox): #時計の更新を行う
        self.__watching_box = box
        self.__cancel_all()
        self.__update_clock(box, self.__clocK_update_interval)

class TimeSetters(tk.Frame):
    def __init__(self, master: tk.Misc):
        tk.Frame.__init__(self, master)
        self.__boxes = list(
            map(
                lambda items, range: SpinInput(self, range, title=items[0]),
                vars(RoutineData()).items(), RoutineData.time_range
            )
        )
        
        for box in self.__boxes:
            box.pack()
                    
    def values(self) -> RoutineData:
        return RoutineData(
            *map(
                lambda box: box.value(),
                self.__boxes
            )
        )
        
    def set(self, time: RoutineData):
        list(
            map(
                lambda box, value: box.set(value),
                self.__boxes, vars(time).values()
            )
        )