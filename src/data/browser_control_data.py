from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import InvalidArgumentException
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

from interface import *
from setting_data import *

class BrowserControlData(IBrowserControlData):
    def __init__(self, setting: SettingData, driver: webdriver = None, wait: WebDriverWait = None) -> None:        
        self.__driver = driver \
            if driver != None \
            else create_driver(SettingData.profile_path(), *setting.web_driver_options)
                        
        self.__wait = wait \
            if wait != None \
            else WebDriverWait(self.__driver, setting.loading_wait_time, 1)
    
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
        
def create_driver(profile: Path, *optional_args) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    option_list = [f'--user-data-dir={profile.parent}', f'--profile-directory={profile.name}', *list(optional_args)]
    for option in option_list:
        if type(option) is str:
            options.add_argument(option)
        else:
            raise ValueError(f'Invalid option: {option}')
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except InvalidArgumentException:
        raise ValueError(f'Invalid options: {option_list}')
    return driver