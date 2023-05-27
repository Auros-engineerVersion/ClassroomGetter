import traceback
import asyncio
from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.gui.application_root import ApplicationRoot

try:
    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()h
    cfg = ApplicationRoot.setup()
    root = ApplicationRoot(min(cfg.nodes), cfg, (500, 300))
    asyncio.run(root.run_async())
    #Settings.save(SettingData.SETTINGFOLDER_PATH, new_cfg)
            
except ChildProcessError as e:
    root.stop()
    print('\nProcess has finished by Hand')
            
except NoSuchWindowException as e:
    root.stop()
    print('\nProcess has finished by Hand')
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    for trace in list(traceback.TracebackException.from_exception(e).format()):
        print(trace)
    
finally:
    print('\033[0m')