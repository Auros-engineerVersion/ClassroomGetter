from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from ..interface import *
from ..my_util import is_none


class BrowserControlData(IBrowserControlData):
    def __init__(self, cfg: ISettingData, driver: webdriver = None, wait: WebDriverWait = None) -> None:        
        self.__driver = is_none(driver, lambda:create_driver(cfg))
        self.__wait = is_none(wait, lambda:WebDriverWait(self.__driver, cfg.loading_wait_time.value, 1))
    
    def __del__(self):
        del self.__wait
        self.__driver.quit()
        del self.__driver
    
    @property
    def driver(self) -> webdriver:
        return self.__driver
    
    @property
    def wait(self) -> WebDriverWait:
        return self.__wait
        
def create_driver(cfg: ISettingData) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    optional_args = cfg.web_driver_options.value
    if not cfg.is_guest():
        optional_args.extend([f'--user-data-dir={cfg.profile_path().parent}', 
                              f'--profile-directory={cfg.profile_path().name}'])
        
    for option in optional_args:
        if type(option) is str:
            options.add_argument(option)
        else:
            raise ValueError(f'Invalid option: {option}')
    
    options.add_experimental_option('prefs', {
        "download.default_directory":str(cfg.save_folder_path.value.absolute()),
        "plugins.always_open_pdf_externally": True
    })
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        #ヘッドレスモードでダウンロードするために以下の処理が必要
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 
                  'params': {'behavior': 'allow', 
                             'downloadPath': str(cfg.save_folder_path.value.absolute())}}
        driver.execute("send_command", params)
    except InvalidArgumentException:
        raise ValueError(f'Invalid options: {optional_args}')
    return driver