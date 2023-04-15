import os
from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.settings import Settings
from src.nodes import Node
from src.browser_controls import BrowserControls

try:
    target_url = 'https://classroom.google.com/' #固定値

    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()
    cfg = Settings.Load(Settings.DefaultSaveFolderPath)
    
    bc = BrowserControls(setting=cfg)
    #プロファイルが指定されているかどうか
    #されていなければログインして指定する
    bc.move(target_url)
    if (target_url not in bc.driver.current_url):
        bc.login_classroom(cfg)
    
    Node.BrowserControl = bc
    
    root = Node(target_url, 0)
    Node.InitializeTree(root)
    Node.ShowTree(root)
    
    cfg.node_list = Node.Nodes
    Settings.Save(cfg)
                
except NoSuchWindowException as e:
    print('\nProcess has finished by Hand')
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    print(e)
    
finally:
    print('\033[0m')