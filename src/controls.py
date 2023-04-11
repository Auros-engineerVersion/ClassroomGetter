from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from re import search
import pyperclip

from . import custum_condition as MyEC
from src.factory import create_driver

class Controls:
    def __init__(self, profile_path: str, profile_name: str) -> None:
        self.driver = create_driver(profile_path, profile_name)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 5)
        pass
    
    def __del__(self):
        del self.wait
        self.driver.quit()
        del self.driver
        pass
    
    def move(self, url: str):
        self.driver.get(url)
    
    def click_all_sections(self):
        def __move_and_click(elem: WebElement):
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            self.driver.execute_script('arguments[0].click()', elem)

        #一つめは3点ボタン、2つめは「リンクをコピー」へのxpath
        xpathes = ["//div[@class='SFCE1b']"]
        buttons = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpathes[0])))
        for button in buttons:
            __move_and_click(button)
        
    def hrefs(self, locator, pattern: str = ''):
        elems = None
        try:
            elems = self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutError as e:
            raise e
        
        unique_links = set() #重複処理のため

        for elem in elems:
            link = str(elem.get_attribute('href'))
            #文字列が見つかれば
            if (search(pattern=pattern, string=link) != None):
                unique_links.add(link)
            
        return unique_links