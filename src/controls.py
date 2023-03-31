from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import InvalidArgumentException
from . import custum_condition as MyEC
from .factory import create_driver

class Controls:
    def __init__(self, profile_path: str, profile_name: str) -> None:
        self.__driver = create_driver(profile_path, profile_name)
        self.__wait = WebDriverWait(self.__driver, 30)
        pass
    
    def __del__(self):
        del self.__wait
        self.__driver.quit()
        del self.__driver
        pass
    
    @staticmethod
    def move(driver: webdriver, url: str):
        try:
            driver.get(url)
        except InvalidArgumentException as e:
            raise e
        
    @staticmethod
    def hrefs(wait: WebDriverWait, *conditions: str):
        elems = wait.until(MyEC.document_state_is((By.TAG_NAME, 'a'), 'complete'))
        links = set()
        
        for elem in elems:
            link = elem.get_attribute('href')
            #全ての条件に合致するなら
            for condition in conditions:
                if (condition in link):
                    links.add(link)
                    
        return links
                
    @classmethod
    def move(cls, url: str):
        Controls.move(cls.__driver, url)
        
    @classmethod
    def hrefs(cls, *conditions: str):
        return Controls.hrefs(cls.__wait, conditions)