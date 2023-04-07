from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def create_driver(profile_path: str, account_name: str) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={profile_path}')
    options.add_argument(f'--profile-directory={account_name}')
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1200,1000)
    return driver

def create_beautifulsoup(html:str):
    soup_obj = BeautifulSoup(html, 'html.parser')
    return soup_obj