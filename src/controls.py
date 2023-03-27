from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .factory import create_driver
import re

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
    
# public
    def move(self, url: str):
        try:
            self._driver.get(url)
        finally:
            return self # Linqライクにするため
        
    def hrefs(self, class_name: str):
        elems = self._wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        links = set()
        for elem in elems:
            link = elem.get_attribute("href")
            #文字列を含むなら
            if ('https://classroom.google.com/u/0/c/' in link):
                if not ('/sp/' in link):
                    links.add(link)
                
        return links