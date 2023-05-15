import traceback
from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.setting.settings import Settings, SettingData
from src.data.nodes import Node
from src.browser.browser_controls import BrowserControl
from src.gui.window import Window

try:
    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()
    cfg = Window.setup()
    new_cfg = Window.RunWindow(min(cfg.node_list), cfg)
    Settings.save(SettingData.SETTINGFOLDER_PATH, new_cfg)
            
except NoSuchWindowException as e:
    print('\nProcess has finished by Hand')
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    for trace in list(traceback.TracebackException.from_exception(e).format()):
        print(trace)
    
finally:
    print('\033[0m')