from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from .factory import create_driver
from urllib.parse import urljoin
import time

class Controls:
    def __init__(self, profile_path: str, profile_name: str) -> None:
        self._driver = create_driver(profile_path, profile_name)
        self._wait = WebDriverWait(self._driver, 30)
        pass
    
    def __del__(self):
        del self._wait
        self._driver.quit()
        del self._driver
        pass
        
# private
    def _set_current_data(self):
        self._current_html = self._driver.page_source.encode('utf-8')
        self._soupObj = bs(self._current_html, 'html.parser')
    
# public
    def move(self, url: str):
        try:
            self._driver.get(url)
            time.sleep(2)
            self._set_current_data()
        finally:
            return self # Linqライクにするため
        
    def hrefs(self, class_name: str):
        hrefs = [value['href'] for value in self._soupObj.find_all('a', class_=class_name)]
        return hrefs
    
    def get_base(self):
        return self._soupObj.find('base')['href']