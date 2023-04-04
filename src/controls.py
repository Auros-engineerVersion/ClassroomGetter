from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import InvalidArgumentException
from time import sleep
from re import search

from . import custum_condition as MyEC
from .factory import create_driver

class Controls:
    def __init__(self, profile_path: str, profile_name: str) -> None:
        self.driver = create_driver(profile_path, profile_name)
        self.wait = WebDriverWait(self.driver, 30, poll_frequency=3)
        pass
    
    def __del__(self):
        del self.wait
        self.driver.quit()
        del self.driver
        pass
    
    def move(self, url: str, wait_time: int = 0):
        try:
            self.driver.get(url)
        except InvalidArgumentException as e:
            raise e
        finally:
            #暗黙的な待機を疑似的に再現したもの
            sleep(wait_time)
    
    @staticmethod
    def hrefs(wait:WebDriverWait, pattern: str):
        elems = wait.until(MyEC.document_state_is((By.TAG_NAME, 'a'), 'complete'))
        unique_links = set() #重複処理のため

        for elem in elems:
            link = elem.get_attribute('href')
            #文字列が見つかれば
            if (search(pattern=pattern, string=link) != None):
                unique_links.add(link)
            
        return unique_links