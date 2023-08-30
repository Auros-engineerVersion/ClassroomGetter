import traceback
import asyncio
from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.gui.application_root import ApplicationRoot

def main():
    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()h
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    cfg_and_bc = ApplicationRoot.setup()
    root = ApplicationRoot(*cfg_and_bc, (400, 300))
    root_run_task = loop.create_task(root.run_async(refresh_rate=12))
    
    try:
        loop.run_until_complete(root_run_task)
        
    except ChildProcessError as e:
            print('\nProcess has finished by Hand')

    except NoSuchWindowException as e:
            print('\nProcess has finished by Hand')
            
    finally:
        root_run_task.cancel()
        asyncio.get_event_loop().close()

try:
    main()
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    for trace in list(traceback.TracebackException.from_exception(e).format()):
        print(trace)
    
finally:
    print('\033[0m')