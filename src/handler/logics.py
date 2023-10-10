import threading

from ..my_util import *
from ..data import *
from ..my_io import *


@higher_order
def root_stop(root, session):
    close_thread = threading.Thread(target=session.close)\
        |pipe|  (lambda t: t.start())

    for thread in [t for t in threading.enumerate() if t not in (threading.main_thread(), close_thread)]:
        thread.join()

        root.destroy()
        close_thread.join()

def e_runner_add_with_thread(event_runner, func):
    thread = threading.Thread(target=func)
    event_runner.add(thread.start)
    
def saving(data):
    try_save(
        file_path=ISettingData.SETTINGFOLDER_PATH.joinpath('setting.json'),
        data=data)

@higher_order
def time_set(node_box, timer, when_reach: Callable):
    """この関数はtime_observe_startを呼び出すため、スレッドが生成される"""
    node_box.time = timer.time
    node_box.time.allow_observe()
    node_box.time.time_observe_start(when_reach)
    
@higher_order
def time_reset(node_box, timer):
    timer.clock_label[TEXT] = NO_DATA
    timer.cancel_all()
    
    node_box.time.reset()
    node_box.time.reject_observe()
    
@higher_order
def time_restart(node_box, timer, when_reach: Callable):
    """この関数はtime_observe_startを呼び出すため、スレッドが生成される"""
    time_reset(node_box, timer)()
    time_set(node_box, timer, when_reach)()
    timer.clock_event_publish(node_box.time)