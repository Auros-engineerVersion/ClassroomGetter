import traceback

from pydrive2.auth import GoogleAuth
from selenium.common.exceptions import NoSuchWindowException

from src.gui.application_root import ApplicationRoot
from src.my_io import *


def main():
    #最初の認証
    #gauth = GoogleAuth()
    #gauth.LocalWebserverAuth()
    
    try:
        path = SettingData.SETTINGFOLDER_PATH.joinpath('setting.json').absolute()
        ApplicationRoot(try_load(path), (400, 300)).mainloop()
    except ChildProcessError or NoSuchWindowException as e:
            print('\nProcess has finished by Hand')

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