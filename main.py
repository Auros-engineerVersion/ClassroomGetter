import traceback
import asyncio
from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.gui.application_root import ApplicationRoot

def main():
    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()h
    
    cfg_and_bc = ApplicationRoot.setup()
    root = ApplicationRoot(*cfg_and_bc, (400, 300))
    try:
        root.mainloop()
        
    except ChildProcessError as e:
            print('\nProcess has finished by Hand')

    except NoSuchWindowException as e:
            print('\nProcess has finished by Hand')

try:
    main()
        
except Exception as e:
    print('\033[31m')
    print(type(e))
    for trace in list(traceback.TracebackException.from_exception(e).format()):
        print(trace)
    
finally:
    print('\033[0m')