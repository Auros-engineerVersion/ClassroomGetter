from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from re import search

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
    
    def title(self):
        #このxpathは固定である
        title_xpath = '//*[@id="yDmH0d"]/c-wiz[1]/div/div/div[5]/div[1]/div/div[2]/h1'
        title = self.wait.until(EC.visibility_of_element_located((By.XPATH, title_xpath))).text
        re_tuple = search('（.*?）', title).span()
        return title[:re_tuple[0]]    
    
    def link_copy_button(self) -> WebElement:
        if ('/t/all' not in self.driver.current_url):
            return None
        
        xpath = "//div[@class='SFCE1b']"
        sections = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    
    def move(self, url: str):
        try:
            self.driver.get(url)
        except InvalidArgumentException as e:
            raise e
    
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