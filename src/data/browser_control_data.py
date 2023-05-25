from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

from src.data.setting_data import SettingData

class BrowserControlData:
    def __init__(self, setting: SettingData, driver: webdriver = None, wait: WebDriverWait = None) -> None:        
        self.driver = driver if (driver != None) else create_driver(SettingData.profile_path())
        self.wait   = wait   if (wait   != None) else WebDriverWait(self.driver, setting.loading_wait_time, 1)
    
    def __del__(self):
        del self.wait
        self.driver.quit()
        del self.driver
        
def create_driver(profile: Path) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={profile.parent}')
    options.add_argument(f'--profile-directory={profile.name}')
        
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(5000,5000)
    return driver