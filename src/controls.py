from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import InvalidArgumentException
from time import sleep

from . import custum_condition as MyEC
from .factory import create_driver

class Controls:
    def __init__(self, profile_path: str, profile_name: str) -> None:
        self.__driver = create_driver(profile_path, profile_name)
        self.__wait = WebDriverWait(self.__driver, 30, poll_frequency=3)
        pass
    
    def __del__(self):
        del self.__wait
        self.__driver.quit()
        del self.__driver
        pass
    
    def move(self, url: str, wait_time: int = 0):
        try:
            self.__driver.get(url)
        except InvalidArgumentException as e:
            raise e
        finally:
            #暗黙的な待機を疑似的に再現したもの
            sleep(wait_time)
        
    def hrefs(self, *conditions: str):
        def __containe(target: str, *conditions: str):
            is_containe = []
            for condition in conditions:
                is_containe.append(target in condition)
            
            #もし全ての条件に合致するなら
            #条件の長さと条件に合致した回数が同じなら
            if (len(condition) == len(is_containe)):
                return target
            
        elems = self.__wait.until(MyEC.document_state_is((By.TAG_NAME, 'a'), 'complete'))
        #aタグ内のhrefを取得する
        #そののち、conditonに合致したlinksを返す
        return map(__containe, map(lambda link : link['href'], elems), conditions)
