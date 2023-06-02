from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from src.interface.i_browser_control_data import *

from src.data.setting_data import SettingData

#options.add_argument("--ignore-certificate-error")
#options.add_argument("--ignore-ssl-errors")
class BrowserControlData(IBrowserControlData):
    def __init__(self, setting: SettingData, driver: webdriver = None, wait: WebDriverWait = None) -> None:        
        self.__driver = driver \
            if driver != None \
            else create_driver(
                SettingData.profile_path(),
                '--ignore-certificate-error', 
                '--ignore-ssl-errors',
                '--headless'
            )
            
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
    option_list = [f'--user-data-dir={profile.parent}', f'--profile-directory={profile.name}', *optional_args]
    for option in option_list:
        options.add_argument(option)
        
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(5000,5000)
    return driver