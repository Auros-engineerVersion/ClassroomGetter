from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import InvalidArgumentException
from time import sleep
import re

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
    def hrefs(wait:WebDriverWait, *conditions):
        def __containe(target: str, *conditions):
            containe_count = 0
            for condition in conditions:
                if (condition in target):
                    containe_count += 1 #条件に合致したなら1増やす
            
            #もし全ての条件に合致するなら
            #条件の長さと条件に合致した回数が同じなら
            if (len(conditions) == containe_count):
                return target
                        
        if (wait == None):
            return
        
        elems = wait.until(MyEC.document_state_is((By.TAG_NAME, 'a'), 'complete'))
        unique_links = set() #重複処理のため

        for elem in elems:
            link = __containe(elem.get_attribute('href'), *conditions)
            if (link != None):
                unique_links.add(link)
            
        return unique_links