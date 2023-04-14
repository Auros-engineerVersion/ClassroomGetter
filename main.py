from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.settings import Settings
from src.nodes import Node
from src.browser_controls import BrowserControls

try:
    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()
    data = Settings.Load()
    
    Node.BrowserControl = BrowserControls()
    
    root = Node(cfg.TARGET_URL, 0)
    Node.InitializeTree(root)
    Node.ShowTree(root)
                
except NoSuchWindowException as e:
    print('\nProcess has finished by Hand')
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    print(e)
    
finally:
    print('\033[0m')