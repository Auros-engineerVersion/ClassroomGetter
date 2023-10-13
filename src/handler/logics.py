import threading

from ..my_util import *
from ..data import *
from ..my_io import *


@higher_order
def root_stop(root, session) -> Callable:
    root.destroy()
    close_thread = threading.Thread(target=session.close)
    close_thread.start()
    
    for thread in [t for t in threading.enumerate() if t not in (threading.main_thread(), close_thread)]:
        thread.join()

@higher_order
def saving(data) -> Callable:
    try_save(
        file_path=ISettingData.SETTING_FOLDER_PATH.joinpath('setting.json'),
        data=data)

def time_set(node_box, timer, when_reach: Callable):
    """この関数はtime_observe_startを呼び出すため、スレッドが生成される"""
    node_box.time = timer.time
    node_box.time.allow_observe()
    node_box.time.time_observe_start(when_reach)
    
def time_reset(node_box, timer):
    timer.clock_label[TEXT] = NO_DATA
    timer.cancel_all()
    
    node_box.time.reset()
    node_box.time.reject_observe()
    
def time_start(node_box, timer, when_reach: Callable):
    """この関数はtime_observe_startを呼び出すため、スレッドが生成される"""
    time_set(node_box, timer, when_reach)
    timer.clock_event_publish(node_box.time)
    
def time_restart(node_box, timer, when_reach: Callable):
    """この関数はtime_observe_startを呼び出すため、スレッドが生成される"""
    time_reset(node_box, timer)
    time_start(node_box, timer, when_reach)
    
def initialize_event_add(event_runner, node_box, session):
    node_box.close()
    event_runner.add(lambda:node_box.initialize(session.next_key_url))