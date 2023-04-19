import os
from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.setting.settings import Settings
from src.browser.nodes import Node
from src.browser.browser_controls import BrowserControls
from src.gui.window import Window

try:
    target_url = 'https://classroom.google.com/' #固定値

    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()
    cfg = Settings.Load(Settings.DefaultSaveFolderPath)
    
    #node_listが何も設定されていないのなら値を取りに行く
    if cfg.node_list == None or len(cfg.node_list) <= 1:
        bc = BrowserControls(setting=cfg)
        #プロファイルが指定されているかどうか
        #されていなければログインして指定する
        bc.move(target_url)
        if (target_url not in bc.driver.current_url):
            bc.login_classroom(cfg)

        Node.BrowserControl = bc
        root = Node('Classroom', target_url, 0)
        Node.InitializeTree(root)
    
        cfg.node_list = Node.Nodes
        Settings.Save(cfg)
        
    root = min(cfg.node_list)
    Window.RunWindow(root)
                
except NoSuchWindowException as e:
    print('\nProcess has finished by Hand')
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    print(e)
    
finally:
    print('\033[0m')