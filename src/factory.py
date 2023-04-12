from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def create_driver(profile_path: str, account_name: str) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if (profile_path != None):
        options.add_argument(f'--user-data-dir={profile_path}')
        
    if (account_name != None):
        options.add_argument(f'--profile-directory={account_name}')
        
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1200,1000)
    return driver