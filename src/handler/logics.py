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