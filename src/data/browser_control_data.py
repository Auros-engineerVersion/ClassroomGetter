from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from ..literals import *
from ..interface import *
from ..my_util import is_none, arrow


class BrowserControlData(IBrowserControlData):
    def __init__(self, cfg: ISettingData, driver: webdriver = None, wait: WebDriverWait = None) -> None:        
        self.__driver: webdriver = is_none(driver, lambda:create_driver(cfg))
        self.__wait: WebDriverWait = is_none(wait, lambda:WebDriverWait(self.__driver, cfg.loading_wait_time[VALUE], 1))
    
        self.download_path_change(cfg.save_folder_path[VALUE], self.__driver)
    
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
    
    @property
    def current_url(self) -> str:
        return self.__driver.current_url
    
    def download_path_change(self, path: Path, driver: webdriver=None) -> Path:
        if driver is None:
            driver = self.__driver
            
        driver.execute(
            driver_command='send_command',
            params={
                'cmd': 'Page.setDownloadBehavior',
                'params': {
                    'behavior': 'allow',
                    'downloadPath': str(path)}})
        
        return path
        
def create_driver(cfg: ISettingData) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    optional_args = cfg.web_driver_options[VALUE]
    if not cfg.is_guest():
        optional_args.extend([f'--user-data-dir={cfg.profile_path.parent}', 
                              f'--profile-directory={cfg.profile_path.name}'])
        
    for option in optional_args:
        options.add_argument(option)
    
    options.add_experimental_option('prefs', {
        "download.default_directory":str(cfg.save_folder_path[VALUE]),
        "plugins.always_open_pdf_externally": True})
    
    try:
        driver = webdriver.Chrome(service=Service(), options=options)\
            |arrow| (lambda d: d.command_executor._commands.update({ #ヘッドレスモードでダウンロードするために以下の処理が必要
                'send_command': ('POST', '/session/$sessionId/chromium/send_command')}))\

    except InvalidArgumentException:
        raise ValueError(f'Invalid options: {optional_args}')
    return driver