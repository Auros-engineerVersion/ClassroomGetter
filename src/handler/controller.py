import threading
from tkinter import Widget

from ..gui import *
from ..my_util import *
from ..data import *
from ..interface import *

from . import logics as lg
from .driver_session import *
from .event_runner import *


def children(widget) -> dict[Widget, type]:
    result = {widget: widget.__class__}
    def _loop(widget):
        for child in widget.winfo_children():
            #インスタンスをkeyにしているので、同一クラスのインスタンスを取得できる
            result.update({child: child.__class__})
            _loop(child)

    _loop(widget)
    return result

def name_of(cls, dic) -> str:
    from_value = [k for k, v in dic.items() if v == cls]
    if len(from_value) == 1:
        #固有のものであればそれを返す
        return from_value[0]
    else:
        return from_value

class Controller:
    def __init__(self, root: ApplicationRoot, session: DriverSession) -> None:
        self.root = root
        self.default_session = session
        self.event_runner: EventRunner = EventRunner()
        
        self.binding(children(root), session)
            
    def binding(self, ins_type: dict[Widget, type], session: DriverSession):
        app_root:           ApplicationRoot = name_of(ApplicationRoot, ins_type)
        setting_frame:      SettingFrame =    name_of(SettingFrame, ins_type)
        node_info_frame:    NodeInfoFrame =   name_of(NodeInfoFrame, ins_type)
        timer:              Timer =           name_of(Timer, ins_type)
        time_setters:       TimeSetters =     name_of(TimeSetters, ins_type)
        node_box:           NodeBox =         name_of(NodeBox, ins_type)
        
#region IO
        setting_frame.on_save(lambda: lg.saving(setting_frame.current_cfg()))
#endregion
        
#region Node管理系
        node_info_frame.on_node_init_btn_press(lambda:
            lg.e_runner_add_with_thread(
                event_runner=self.event_runner,
                func=lambda:
                    node_info_frame.node_box.initialize(
                        aqcuire=session.next_key_url)))
        
        #監視しているNodeBoxを更新する
        timer.on_time_set_btn_press(lambda:
            timer.clock_event_publish(
                dead_line=time_setters.value(),
                interval_ms=10))
        
        timer.on_time_reset_btn_press(f=timer.clock_reset)
        
        #この関数はなくし、できれば無名関数で書きたい
        #しかしながら無名関数内での代入はできなかった
        #これは妥協である
        def __set_box_to_info_frame(other: NodeBox):
            node_info_frame.node_box = other
        
        #最初に表示されるNodeBoxのeventを設定する
        node_box.on_click_this(lambda:__set_box_to_info_frame(node_box))
        node_box.on_expand(
            lambda n: n.on_click_this(lambda: __set_box_to_info_frame(n)))
#endregion
            
        app_root.on_loop_end(self.event_runner.run_all)
        app_root.on_stop(lambda:
            lg.root_stop(app_root, session)\
                |pipe| (lambda _: lg.saving(setting_frame.current_cfg())))
        
    def run_applicaiton(self):
        self.root.run()