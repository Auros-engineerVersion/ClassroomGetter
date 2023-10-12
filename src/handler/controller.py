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
        self.about_node(ins_type, session)
        self.about_app_root(ins_type, session)
        
    def about_node(self, ins_type: dict[Widget, type], session: DriverSession):
        node_info_frame:    NodeInfoFrame =   name_of(NodeInfoFrame, ins_type)
        timer:              Timer =           name_of(Timer, ins_type)
        node_box:           NodeBox =         name_of(NodeBox, ins_type)

        node_info_frame.on_node_init_btn_press(
            lg.initialize_event_add(
                self.event_runner,
                node_info_frame.node_box,
                session))
        
        node_info_frame.on_node_change(
            lg.time_restart(
                node_box=node_info_frame.node_box,
                timer=timer,
                when_reach=lg.initialize_event_add(
                    event_runner=self.event_runner,
                    node_box=node_info_frame.node_box,
                    session=session)))
        
        #監視しているNodeBoxを更新する
        timer.on_time_set_btn_press(
            lg.time_restart(
                node_box=(box := node_info_frame.node_box),
                timer=timer,
                when_reach= #時間が来たら実行する関数
                    lg.initialize_event_add(
                        event_runner=self.event_runner,
                        node_box=box,
                        session=session)))
                
        timer.on_time_reset_btn_press(
            lg.time_reset(
                node_box=node_info_frame.node_box,
                timer=timer))
        
        @higher_order
        def __set_box_to_info_frame(other: NodeBox):
            node_info_frame.node_box = other
        
        #最初に表示されるNodeBoxのeventを設定する
        node_box.on_click_this(__set_box_to_info_frame(node_box))
        node_box.on_expand(
            lambda n: n.on_click_this(__set_box_to_info_frame(n)))
        
    def about_app_root(self, ins_type: dict[Widget, type], session: DriverSession):
        app_root:           ApplicationRoot = name_of(ApplicationRoot, ins_type)
        setting_frame:      SettingFrame =    name_of(SettingFrame, ins_type)
        node_info_frame:    NodeInfoFrame =   name_of(NodeInfoFrame, ins_type)
        timer:              Timer =           name_of(Timer, ins_type)
        
        setting_frame.on_save(lambda:lg.saving(setting_frame.current_cfg()))
            
        app_root.on_loop_end(self.event_runner.run_all)
        app_root.on_stop(lambda:
            lg.time_reset(node_box=node_info_frame.node_box, timer=timer)
            |pipe| lg.saving(setting_frame.current_cfg())
            |pipe| lg.root_stop(app_root, session))

    def run_applicaiton(self):
        self.root.run()