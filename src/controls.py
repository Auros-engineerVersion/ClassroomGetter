from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from re import search

from src.factory import create_driver

class Controls:
    def __init__(self, profile_path: str, profile_name: str) -> None:
        self.driver = create_driver(profile_path, profile_name)
        self.wait = WebDriverWait(self.driver, 3)
        pass
    
    def __del__(self):
        del self.wait
        self.driver.quit()
        del self.driver
        pass
    
    def move(self, url: str):
        self.driver.get(url)
    
    def click_all_sections(self, func, locator_and_pattern: tuple):
        def __move_and_click(elem: WebElement):
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            self.driver.execute_script('arguments[0].click()', elem)

        #一つめは3点ボタン、2つめは「リンクをコピー」へのxpath
        links = []
        xpathes = ["//div[@class='SFCE1b']"]
        
        try:
            buttons = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpathes[0])))
            
        except TimeoutException:
            return []
        
        self.wait._timeout /= 10 #ファイルの読み込みは早いため
        for button in buttons:
            __move_and_click(button)
            links.extend(func()(*locator_and_pattern))
            
        self.wait._timeout *= 10 #元に戻す
        return links
        
    def hrefs(self):
        def __get_hrefs(locator, pattern: str = ''):
            unique_links = set() #重複処理のため
            try:
                elems = self.wait.until(EC.presence_of_all_elements_located(locator))
            except TimeoutException:
                return unique_links
            
            for elem in elems:
                link = str(elem.get_attribute('href'))
                #文字列が見つかれば
                if (search(pattern, string=link) != None):
                    unique_links.add(link)
            return unique_links
        
        return __get_hrefs