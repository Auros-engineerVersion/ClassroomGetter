import traceback
from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.setting.settings import Settings
from src.data.nodes import Node
from src.browser.browser_controls import BrowserControl
from src.gui.window import Window

try:
    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()
    cfg = Settings.load(Settings.DEFAULT_SAVEFOLDER_PATH)
    bc = BrowserControl(setting=cfg)
    Node.BrowserControl = bc
        
    Settings.validate_data(cfg, bc)
        
    root = min(cfg.node_list) #tree_height == 0のものをrootとする
    Window.RunWindow(root)
                
except NoSuchWindowException as e:
    print('\nProcess has finished by Hand')
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    for trace in list(traceback.TracebackException.from_exception(e).format()):
        print(trace)
    
finally:
    Settings.save(cfg)
    print('\033[0m')