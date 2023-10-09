import traceback

from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.gui.application_root import *
from src.data import BrowserControlData as bc_data
from src.my_io import *
from src.handler import *


def setup_profile(cfg: ISettingData, warning = identity):
    if cfg.is_current_user() or cfg.is_guest():
        return cfg
    else:
        warning()
        cfg.profile = ProfileForm().pop_up()
        return setup_profile(
            cfg, 
            lambda: messagebox.showwarning(title=WARNING, message=PROFILE_WARNING))

def set_env(cfg: ISettingData) -> tuple[ISettingData, DriverSession]:
    default_session = DriverSession(
        bc=(bc := bc_data(cfg)),
        save_dir=cfg.save_folder_path[VALUE],
    )
    
    if not cfg.is_guest():
        classroom_login(bc, *cfg.profile)
        
    return cfg, default_session

def main():
    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()
    
    path = SettingData.SETTINGFOLDER_PATH.joinpath('setting.json').absolute()
    cfg, default_session = set_env(setup_profile(try_load(path)))
    root = ApplicationRoot(cfg, (400, 300))
    try:
        Controller(root, default_session).run_applicaiton()
        
    except ChildProcessError or NoSuchWindowException as e:
            print('\nProcess has finished by Hand')
            
    finally:
        print('Process has finished')

try:
    if __name__ == '__main__':
        main()
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    for trace in list(traceback.TracebackException.from_exception(e).format()):
        print(trace)
    
finally:
    print('\033[0m')