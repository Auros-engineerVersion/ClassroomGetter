import os
import traceback
from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.setting.settings import Settings
from src.browser.nodes import Node
from src.browser.browser_controls import BrowserControl
from src.gui.window import Window

try:
    target_url = 'https://classroom.google.com/' #固定値

    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()
    cfg = Settings.load(Settings.DefaultSaveFolderPath)
    bc = BrowserControl(setting=cfg)
    Node.BrowserControl = bc

    #node_listが何も設定されていないのなら値を取りに行く
    if not cfg.is_current_data():
        #プロファイルが指定されているかどうか
        #されていなければログインして指定する
        bc.move(target_url)
        if (target_url not in bc.driver.current_url):
            bc.login_classroom(cfg)

        root = Node('Classroom', target_url, 0)
        root.initialize_tree()
    
        cfg.node_list = Node.Nodes
        Settings.save(cfg)
        
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