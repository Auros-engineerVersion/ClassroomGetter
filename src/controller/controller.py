from tkinter import Widget

from ..gui import *
from ..my_util import *
from ..data import *
from ..interface import *


def children(widget) -> Iterable:
    widgets = {}
    def _loop(widget: Widget) -> dict[str, Widget]:
        nonlocal widgets
        for w in widget.winfo_children():
            widgets.update({w.__class__.__name__: w})
            _loop(w)

    return _loop(widget)

class Controller:
    def __init__(self, root: ApplicationRoot) -> None:
        self.root = root
        self.binding(children(root))
            
    def binding(self, name_ins: dict[str, Widget]):
        setting_frame:      SettingFrame =  name_ins.get(name_of(SettingFrame))
        node_info_frame:    NodeInfoFrame = name_ins.get(name_of(NodeInfoFrame))
        timer:              Timer =         name_ins.get(name_of(Timer))
        node_box:           NodeBox =       name_ins.get(name_of(NodeBox))

#region 設定管理系
        setting_frame.on_save(lambda: 
            setting_frame.save_cfg(
                file_path=ISettingData.SETTINGFOLDER_PATH.joinpath('setting.json')))
#endregion
        
#region Node管理系
        node_info_frame.on_node_init_btn_press(
            f=node_info_frame.__node_box.initialize)
        
        #監視しているNodeBoxを更新する
        timer.on_time_set_btn_press(lambda:
            timer.clock_event_publish(
                dead_line=timer.__time_setters.value(),
                when_reach=node_info_frame.__node_box.initialize,
                interval_ms=10))
        
        timer.on_time_reset_btn_press(f=timer.clock_reset)
        
#endregion
        
    def run_applicaiton(self):
        self.root.mainloop()