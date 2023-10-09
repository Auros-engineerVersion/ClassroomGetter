import asyncio
import tkinter as tk

from ....data import *
from ....literals import *
from ....my_util import arrow, is_none
from ..info_boxes import *


class NodeInfoFrame(tk.Frame):
    def __init__(self, master: tk.Misc, node_box: NodeBox = None):
        tk.Frame.__init__(self, master, background='green')
        self.__node_box = node_box
        
        #keyの表示
        self.__key_label = tk.Label(self, text=is_none(node_box.text, NO_DATA))\
            |arrow| (lambda l: l.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=5))
            
        #urlの表示
        self.__url_label = tk.Label(self, text=is_none(node_box.url, NO_DATA))\
            |arrow| (lambda l: l.pack(side=tk.TOP))
            
        #ボタンが押されたら、監視中のNodeBoxからinitialize_treeを実行する
        self.__init_btn = tk.Button(self, text=RUN)\
            |arrow| (lambda b: b.pack(side=tk.BOTTOM, fill=tk.X))
                        
        #保存の際、そのNodeをパスに含めるかどうかを設定する
        self.__check_var = tk.BooleanVar(value=node_box.include_this_to_path)
        tk.Checkbutton(self,
            text=INCLUDE_THIS_IN_PATH,
            variable=self.__check_var,
            command=lambda: self.on_change_check_value(self.__check_var))\
            |arrow| (lambda c: c.pack(side=tk.BOTTOM, fill=tk.X))
                        
        #次回の更新までの時間を表示する
        self.__timer: Timer = Timer(self, node_box=self.__node_box)\
            |arrow| (lambda t: t.pack(side=tk.TOP))
        
        #全てのNodeに対して、時計を動かす
        #dead_lineが既定の時間の場合、この関数は何もしない
        Node.root().serach()(
            func=lambda n: self.__timer.clock_event_publish(
                dead_line=n.next_init_time,
                interval_ms=10))
    
    @property    
    def node_box(self) -> NodeBox:
        return self.__node_box
    
    @node_box.setter
    def node_box(self, box: NodeBox):
        self.__key_label[TEXT] = box.text
        self.__url_label[TEXT] = box.url
        self.__check_var.set(box.include_this_to_path)
        self.__node_box = box
        self.__timer.watching_box = box
        
    def change_state(self, state: str, text: str):
        self.__init_btn[STATE] = state
        self.__init_btn[TEXT] = text
        self.__init_btn.update()
        
    def on_change_check_value(self, boolean_var: tk.BooleanVar):
        self.__node_box.include_this_to_path = boolean_var.get()
        
    def on_node_init_btn_press(self, f, **kwargs):
        self.__init_btn.bind(BUTTON_PRESS, lambda _: f(**kwargs))
        
class Timer(tk.Frame):
    def __init__(self, master: tk.Misc, node_box: NodeBox):
        tk.Frame.__init__(self, master, background='yellow')
        self.__node_box: NodeBox = node_box
        self.__events: list[int] = []
        
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
        self.__time_setters: TimeSetters = TimeSetters(self)\
            |arrow| (lambda t: t.pack(side=tk.LEFT))
        
        #時間指定ボタン    
        self.__time_set_btn = tk.Button(time_set_frame, text='この時間に指定する')\
            |arrow| (lambda b: b.pack(side=tk.RIGHT))
        
        #時間のリセット
        self.__time_reset_btn = tk.Button(time_set_frame, text=RESET)\
            |arrow| (lambda b: b.pack(side=tk.RIGHT))
                    
    @property
    def watching_box(self):
        return self.__node_box
    
    @watching_box.setter
    def watching_box(self, box: NodeBox):
        self.__cancel_all()
        self.__node_box = box
        self.__time_setters.set(box.time)
        self.clock_event_publish(box.time)
        
    def __cancel_all(self):
        #保持されたイベントを全てキャンセルする
        for id in self.__events:
            self.after_cancel(id)
        self.__events.clear()
                
    def clock_event_publish(self, dead_line: IRoutineData, interval_ms: int = 500):
        """boxの残り時間を監視し、表示する
        Args:
            dead_line (IRoutineData): 残り時間
            interval_ms (int): 更新間隔
        """

        #値が初期値でないかチェック
        if not dead_line.is_current():
            return
        
        if (remaine_time := dead_line.remaine()) == timedelta():
            self.clock_label[TEXT] = NO_DATA
        else:
            self.clock_label[TEXT] = remaine_time
        
        #発行されたイベントのidを保存する
        self.__events.append(
            self.after(interval_ms, self.clock_event_publish, dead_line, interval_ms))

    def clock_reset(self):
        self.__node_box.time_reset()
        self.__cancel_all()
        self.clock_label[TEXT] = NO_DATA

    def on_time_set_btn_press(self, f, **kwargs):
        self.__time_set_btn.bind(BUTTON_PRESS, lambda _: f(**kwargs))
        
    def on_time_reset_btn_press(self, f, **kwargs):
        self.__time_reset_btn.bind(BUTTON_PRESS, lambda _: f(**kwargs))

class TimeSetters(tk.Frame):
    def __init__(self, master: tk.Misc):
        tk.Frame.__init__(self, master)
        self.__boxes = list(
            map(
                lambda items, range: SpinInput(from_to=range, master=self, title=items),
                vars(RoutineData()).keys(), RoutineData.time_range))
        
        for box in self.__boxes:
            box.pack()
                    
    def value(self) -> RoutineData:
        return RoutineData(*[int(b.get()) for b in self.__boxes])
        
    def set(self, time: RoutineData):
        for box, v in zip(self.__boxes, vars(time).values()):
            box.set(v)