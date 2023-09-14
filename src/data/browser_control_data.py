from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from ..my_util import is_none
from ..interface import *

class BrowserControlData(IBrowserControlData):
    def __init__(self, cfg: ISettingData, driver: webdriver = None, wait: WebDriverWait = None) -> None:        
        self.__driver = is_none(driver, create_driver(cfg))
        self.__wait = is_none(wait, WebDriverWait(self.__driver, cfg.loading_wait_time.value, 1))
    
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
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except InvalidArgumentException:
        raise ValueError(f'Invalid options: {optional_args}')
    return driver